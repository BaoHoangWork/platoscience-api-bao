from django.db import models

class QuestionOption(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='options')
    label = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.label
    
    class Meta:
        db_table = 'assessments_question_option'
