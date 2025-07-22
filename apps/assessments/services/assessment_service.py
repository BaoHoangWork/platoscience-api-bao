from django.utils import timezone
from datetime import timedelta
from apps.assessments.models.question_model import Question
from apps.assessments.models.question_option_model import QuestionOption
from apps.assessments.repositories.assessment_repository import AssessmentRepository
from apps.assessments.services.assessment_answer_service import AssessmentAnswerService
from apps.assessments.services.question_option_service import QuestionOptionService
from apps.assessments.services.question_service import QuestionService
from apps.common.base_service import BaseService
from django.db import transaction
import requests
from apps.common.constants import ASSESSMENT_INTERVAL, AI_BASE_URL

class AssessmentService(BaseService):
    def __init__(self):
        super().__init__(AssessmentRepository())

    def get_all_by_user(self, user):
        return self.repository.get_all_by_user(user)

    def get_latest_by_user(self, user):
        return self.repository.get_latest_by_user(user)

    def is_valid_time(self, user):
        latest_assessment = self.repository.model.objects.filter(user=user).order_by('-created_at').first()
        if not latest_assessment:
            return {"is_valid":True, "next_valid_time": None}  
        now = timezone.now()
        next_valid_time = latest_assessment.created_at + timedelta(weeks=ASSESSMENT_INTERVAL)
        is_valid = now >= next_valid_time
        return {"is_valid": is_valid, "next_valid_time": next_valid_time}

    def create_with_answer(self, assessment_data, user):
        answers_data = assessment_data.pop("answers", [])
        
        print(answers_data)
        
        # Calculate PHQ and BDI scores
        phq_questions = QuestionService().group_questions_by_category(requested_category="phq", answers_data=answers_data)
        bdi_questions = QuestionService().group_questions_by_category(requested_category="bdi", answers_data=answers_data)
        phq_score = QuestionOptionService().sum_of_values(phq_questions)
        bdi_score = QuestionOptionService().sum_of_values(bdi_questions)

        # Get plato score & severity
        try:
            url = f"{AI_BASE_URL}/assess/"
            payload = {
                "scores": [
                    {
                        "scale": "PHQ-9",
                        "score": phq_score
                    },
                    {
                        "scale": "BDI-II",
                        "score": bdi_score
                    }
                ]
            }
            headers = {'Content-Type': 'application/json'}
            response = requests.request("POST", url, headers=headers, json=payload)
            if response.status_code == 200:
                data = response.json()
                severity = data.get("severity_value")
                plato_score = data.get("plato_score")
            else:
                raise ValueError(
                f"Validation Error: {response.text}"
            )
        except Exception as e:
            raise Exception(f"Error retrieving plato_score and severity with score PHQ-9 ({phq_score}) and BDI-II ({bdi_score}): {str(e)}")

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

                return assessment
        except Exception as e:
            raise Exception(f"Error creating assessment: {str(e)}")