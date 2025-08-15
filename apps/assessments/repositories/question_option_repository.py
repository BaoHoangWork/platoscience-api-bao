from apps.assessments.models import QuestionOption
from apps.common.base_repository import BaseRepository

class QuestionOptionRepository(BaseRepository):
    def __init__(self):
        super().__init__(QuestionOption)
