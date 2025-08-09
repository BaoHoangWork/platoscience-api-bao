from rest_framework import serializers
from apps.assessments.models import AssessmentCheckinAnswer
from apps.assessments.serializers.question_serializer import QuestionSerializer
from apps.assessments.serializers.question_option_serializer import QuestionOptionSerializer

class AssessmentCheckinAnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)
    selected_option = QuestionOptionSerializer(read_only=True)

    class Meta:
        mode = AssessmentCheckinAnswer
        fields = [
            'id',
            'question',
            'answer',
            'selected_option',
            'checkin_date'
        ]
    
class CheckInHistoryDaySerializer(serializers.Serializer):
    date = serializers.DateField()
    answers = AssessmentCheckinAnswerSerializer(many=True)