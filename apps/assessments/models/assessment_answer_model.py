from django.db import models
from apps.assessments.models.assessment_model import Assessment
from apps.assessments.models.question_model import Question

class AssessmentAnswer(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='questions')
    answer = models.TextField()
    index = models.IntegerField()

    class Meta:
        db_table = 'assessments_assessment_answer'
