from apps.assessments.models import Assessment
from apps.common.base_repository import BaseRepository

class AssessmentRepository(BaseRepository):
    def __init__(self):
        super().__init__(Assessment)

    def get_all_by_user(self, user):
        return self.filter(user=user).select_related('user', 'protocol').prefetch_related('answers', 'suggested_protocols')
    
    def get_latest_by_user(self, user):
        return (self.filter(user=user)
                    .select_related('protocol')
                    .prefetch_related('suggested_protocols', 'answers')
                    .order_by('-created_at')
                    .first())
