from rest_framework import serializers
from apps.assessments.models import Question
from apps.assessments.serializers.question_option_serializer import QuestionOptionSerializer

class QuestionSerializer(serializers.ModelSerializer):
    options = QuestionOptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = [
         'id',
         'name',
         'content',
         'description',
         'category',
         'options',
         'type'
        ]
        read_only_fields = ['id', 'index']
    
