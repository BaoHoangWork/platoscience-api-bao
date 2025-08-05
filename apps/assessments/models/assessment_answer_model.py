from django.db import models
from apps.assessments.models.assessment_model import Assessment
from apps.assessments.models.question_model import Question
from apps.assessments.models.question_option_model import QuestionOption
class AssessmentAnswer(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='questions')
    answer = models.TextField(null=True, blank=True)
    selected_option = models.ForeignKey(QuestionOption, on_delete=models.SET_NULL, blank=True, null=True, related_name='option')
    index = models.IntegerField()
    is_checkin = models.BooleanField(default=False)
    checkin_date = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'assessments_assessment_answer'
