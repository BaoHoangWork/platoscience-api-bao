from django.db import models
from apps.assessments.models.assessment_model import Assessment
from apps.assessments.models.question_model import Question
from apps.assessments.models.question_option_model import QuestionOption
class AssessmentCheckinAnswer(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='checkin_answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='checkin_answers')
    answer = models.TextField(null=True, blank=True)
    selected_option = models.ForeignKey(QuestionOption, on_delete=models.SET_NULL, blank=True, null=True, related_name='checkin_selected_options')
    checkin_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = 'assessments_checkin_answer'

    def save(self, *args, **kwargs):
        if self.question.category != 'check-in':
            raise ValueError("Only 'check-in' category questions are allowed.")
        super().save(*args, **kwargs)