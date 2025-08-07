from apps.assessments.models import AssessmentAnswer
from apps.common.base_repository import BaseRepository
from django.utils import timezone
from datetime import timedelta

class AssessmentAnswerRepository(BaseRepository):
    def __init__(self):
        super().__init__(AssessmentAnswer)

    def has_checkin_today(self, assessment):
        now = timezone.now()
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        return self.model.objects.filter(
            assessment=assessment,
            is_checkin=True,
            checkin_date__gte=start_of_day,
            checkin_date__lte=now
        ).exists()