from django.utils import timezone
from datetime import timedelta
from apps.assessments.models.question_model import Question
from apps.assessments.models.question_option_model import QuestionOption
from apps.assessments.repositories.assessment_repository import AssessmentRepository
from apps.assessments.serializers.assessment_serializer import AssessmentSerializer
from apps.assessments.services.assessment_answer_service import AssessmentAnswerService
from apps.assessments.services.question_option_service import QuestionOptionService
from apps.assessments.services.question_service import QuestionService
from apps.common.base_service import BaseService
from django.db import transaction
import requests
from apps.common.constants import ASSESSMENT_INTERVAL, AI_BASE_URL, MAX_TOKENS

class AssessmentService(BaseService):
    def __init__(self):
        super().__init__(AssessmentRepository())

    def get_all_by_user(self, user):
        return self.repository.get_all_by_user(user)

    def get_latest_by_user(self, user):
        return self.repository.get_latest_by_user(user)

    def end_assessment_period(self):
        four_weeks_ago = timezone.now() - timedelta(weeks=4)
        two_weeks_ago = timezone.now() - timedelta(weeks=2)
        first_result = self.repository.filter(protocol_selected_date__lt=four_weeks_ago,stopped_date__isnull=True)
        second_result = self.repository.filter(
            protocol_selected_date__isnull=True,
            created_at__lt=two_weeks_ago,
            stopped_date__isnull=True
        )
        result = first_result | second_result
        return result.update(stopped_date=timezone.now())
    
    def end_assessment(self, user, reason):
        latest = self.get_latest_by_user(user)
        if latest:
            latest.stopped_date = timezone.now()
            latest.stop_reason = reason
            latest.save()
            return latest
        return None
        
    def is_valid_time(self, user):
        latest_assessment = self.repository.model.objects.filter(user=user).order_by('-created_at').first()
        if not latest_assessment:
            return {"is_valid":True, "next_valid_time": None}  
        now = timezone.now()
        next_valid_time = latest_assessment.created_at + timedelta(seconds=ASSESSMENT_INTERVAL)
        is_valid = now >= next_valid_time
        return {"is_valid": is_valid, "next_valid_time": next_valid_time}

    def _calculate_scores(self, answers_data):
        phq_questions = QuestionService().group_questions_by_category("phq", answers_data)
        bdi_questions = QuestionService().group_questions_by_category("bdi", answers_data)
        phq_score = QuestionOptionService().sum_of_values(phq_questions)
        bdi_score = QuestionOptionService().sum_of_values(bdi_questions)
        return phq_score, bdi_score
    
    def _get_plato_score_and_severity(self, phq_score, bdi_score):
        url = f"{AI_BASE_URL}/assess/"
        payload = {
            "scores": [
                {"scale": "PHQ-9", "score": phq_score},
                {"scale": "BDI-II", "score": bdi_score}
            ]
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code != 200:
            raise ValueError(f"Validation Error: {response.text}")

        data = response.json()
        return data.get("plato_score"), data.get("severity_value")
    
    def _analyze_depression(self, answers_data):
        analytic_questions = QuestionService().group_questions_by_category("analytic", answers_data)
        query = analytic_questions[0]["answer"]
        
        url = f"{AI_BASE_URL}/analyze-depression/"
        payload = {"query": query, "max_tokens": MAX_TOKENS}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code != 200:
            raise ValueError(f"Validation Error: {response.text}")

        data = response.json()
        return data.get("depression_type"), data.get("analysis")

    def _is_reached_limit(self, user):
        last_four = self.filter(user=user).order_by('-created_at')[:4]
        if len(last_four) < 4:
            return False
        created_time = last_four[3].created_at
        diff = timezone.now() - created_time 
        print(diff.total_seconds())
        if diff.total_seconds() / 60 < 60:
            return True
        else:
            return False
            

    def create_with_answer(self, assessment_data, user):
        """
        Create a new assessment, save answers, calculate scores,
        and retrieve depression analysis, plato score and severity via API AI.

        Args:
            assessment_data (dict): Data containing answers.
            user (User): The user who is creating the assessment.

        Returns:
            dict: {
                "assessment": Assessment instance,
                "depression_type": str,
                "analysis": str
            }
        """
        if self._is_reached_limit(user=user):
            raise Exception("Error: User reached rate limit.")
        
        answers_data = assessment_data.pop("answers", [])
        
        phq_score, bdi_score = self._calculate_scores(answers_data)
    
        try:
            plato_score, severity = self._get_plato_score_and_severity(phq_score, bdi_score)
        except Exception as e:
            raise Exception(f"Error retrieving plato_score and severity: {str(e)}")

        try:
            depression_type, analysis = self._analyze_depression(answers_data)
        except Exception as e:
            raise Exception(f"Error analyzing depression: {str(e)}")
        
        record = self.filter(user=user).order_by('-created_at').first()
        if record:
            record.stopped_date = timezone.now()
            record.save()

        try:
            with transaction.atomic():
                assessment = self.create(
                    **assessment_data, 
                    user=user, 
                    phq_score=phq_score, 
                    bdi_score=bdi_score, 
                    severity=severity,
                    plato_score=plato_score
                )
                for answer in answers_data:
                    QuestionOptionService().validate(answer)
                    AssessmentAnswerService().create(**answer, assessment=assessment)
                
                return {
                    "assessment" : assessment, 
                    "depression_type" : depression_type, 
                    "analysis" : analysis
                }
        except Exception as e:
            raise Exception(f"Error creating assessment: {str(e)}")