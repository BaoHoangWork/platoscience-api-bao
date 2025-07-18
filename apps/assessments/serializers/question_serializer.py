from rest_framework import serializers
from apps.assessments.models import Question

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
         'name',
         'content',
         'description',
         'category',
        ]
        read_only_fields = ['id', 'index']
    
