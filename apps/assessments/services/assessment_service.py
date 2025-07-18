from django.utils import timezone
from datetime import timedelta
from apps.assessments.models.assessment_model import Assessment
from apps.assessments.repositories.assessment_repository import AssessmentRepository
from apps.assessments.services.assessment_answer_service import AssessmentAnswerService
from apps.assessments.services.suggested_protocol_service import SuggestedProtocolService
from apps.common.base_service import BaseService
from django.db import transaction

ASSESSMENT_INTERVAL = 4

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

    def create_with_answer_protocol(self, assessment_data, answers_data, suggested_protocol_data):
        try:
            with transaction.atomic():
                assessment = self.create(**assessment_data)

                for answer in answers_data:
                    AssessmentAnswerService().create(assessment=assessment, **answer)
                
                SuggestedProtocolService().create_suggested_protocols(assessment=assessment, **suggested_protocol_data)

                return assessment
        except Exception as e:
            raise Exception(f"Error creating assessment: {str(e)}")