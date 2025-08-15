from django.db import models

class UserHealthData(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='health_data')

    sleep_start_datetime = models.DateTimeField()
    sleep_end_datetime = models.DateTimeField()
    sleep_duration = models.DurationField()

    steps = models.IntegerField()
    weight = models.FloatField(help_text="Weight in kilograms")

    data_start_datetime = models.DateTimeField()
    data_end_datetime = models.DateTimeField()

    def __str__(self):
        return f"Health data for {self.user.email} ({self.data_start_datetime} - {self.data_end_datetime})"