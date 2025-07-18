from apps.assessments.models import AssessmentAnswer
from apps.common.base_repository import BaseRepository

class AssessmentAnswerRepository(BaseRepository):
    def __init__(self):
        super().__init__(AssessmentAnswer)