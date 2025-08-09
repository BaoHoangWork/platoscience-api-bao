from apps.assessments.repositories.assessment_answer_repository import AssessmentAnswerRepository
from apps.common.base_service import BaseService


class AssessmentAnswerService(BaseService):
    def __init__(self):
        super().__init__(AssessmentAnswerRepository())