from rest_framework import serializers
from apps.assessments.models import AssessmentAnswer
from apps.assessments.serializers.question_serializer import QuestionSerializer
from apps.assessments.serializers.question_option_serializer import QuestionOptionSerializer

class CheckInAnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)
    selected_option = QuestionOptionSerializer(read_only=True)

    class Meta:
        model = AssessmentAnswer
        fields = [
            'id',
            'question',
            'answer',
            'selected_option',
            'index',
        ]

class CheckInHistoryDaySerializer(serializers.Serializer):
    date = serializers.DateField()
    answers = CheckInAnswerSerializer(many=True)
