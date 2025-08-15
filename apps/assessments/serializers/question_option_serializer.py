from rest_framework import serializers
from apps.assessments.models import QuestionOption

class QuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOption
        fields = [
            'id',
            'label',
            'value',
        ]
        read_only_fields = ['id', 'index']
