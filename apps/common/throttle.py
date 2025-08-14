from datetime import datetime, timedelta, timezone
from rest_framework.throttling import SimpleRateThrottle
from apps.assessments.models import Assessment  


class LimitAssessThrottle(SimpleRateThrottle):
    scope = 'limit'

    def get_cache_key(self, request, view):
        """
        Return user ID for throttling.
        """
        if not request.user or not request.user.is_authenticated:
            return None
        return request.user.pk  

    def _now_utc_ts(self):
        """
        Return current UTC timestamp as a UNIX timestamp.
        """
        return int(datetime.now(timezone.utc).timestamp())

    def allow_request(self, request, view):
        """
        Check if user reaches the limit with database
        """
        user_id = self.get_cache_key(request, view)
        if user_id is None:
            return False

        now = datetime.now(timezone.utc)
        rate, duration = self.parse_rate(self.get_rate())

        # Fixed window start time
        window_start_ts = now.timestamp() - (now.timestamp() % duration)
        window_start_dt = datetime.fromtimestamp(window_start_ts, tz=timezone.utc)

        # Count records in database for this window
        count = Assessment.objects.filter(
            user_id=user_id,
            created_at__gte=window_start_dt
        ).count()

        if count >= rate:
            self.window_start = int(window_start_ts)
            self.duration = duration
            return False

        return True

    def wait(self):
        """
        Seconds until next reassess.
        """
        if not hasattr(self, 'window_start') or not hasattr(self, 'duration'):
            return None
        return max(0, (self.window_start + self.duration) - self._now_utc_ts())

    def get_current_state(self, request, view):
        """
        Get current state of reassessment without increasing count.
        """
        user_id = self.get_cache_key(request, view)
        if user_id is None:
            return False, None
        
        rate, duration = self.parse_rate(self.get_rate())

        window_start_ts = self._now_utc_ts() - (self._now_utc_ts() % duration)
        window_start_dt = datetime.fromtimestamp(window_start_ts, tz=timezone.utc)

        count = Assessment.objects.filter(
            user_id=user_id,
            created_at__gte=window_start_dt
        ).count()

        if count >= rate:
            remain_time = window_start_ts + duration - self._now_utc_ts()
            return False, remain_time

        return True, None
