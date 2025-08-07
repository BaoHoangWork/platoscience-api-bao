from apps.assessments.models import AssessmentAnswer
from apps.common.base_repository import BaseRepository
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import TruncDate

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
    
    def get_checkin_answers_grouped_by_date(self, assessment):
        qs = self.model.objects.filter(
            assessment=assessment,
            is_checkin=True
        ).annotate(checkin_day=TruncDate('checkin_date')).order_by('-checkin_date')
        history = {}
        for ans in qs:
            day = ans.checkin_day
            if day not in history:
                history[day] = []
            history[day].append(ans)
        return history