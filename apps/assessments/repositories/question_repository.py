from apps.assessments.models import Question
from apps.common.base_repository import BaseRepository

class QuestionRepository(BaseRepository):
    def __init__(self):
        super().__init__(Question)

    def get_all(self):
        return self.model.objects.prefetch_related('options').all()
