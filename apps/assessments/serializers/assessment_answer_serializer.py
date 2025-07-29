from rest_framework import serializers
from apps.assessments.models import AssessmentAnswer, Question, QuestionOption
from apps.assessments.serializers.question_serializer import QuestionSerializer
from apps.assessments.serializers.question_option_serializer import QuestionOptionSerializer

class AssessmentAnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)
    assessment = serializers.PrimaryKeyRelatedField(read_only=True)
    selected_option = QuestionOptionSerializer(read_only=True)

    class Meta:
        model = AssessmentAnswer
        fields = [
            'id',
            'assessment',
            'question',
            'answer',
            'selected_option',
            'index',
        ]

class CreateAssessmentAnswerSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    assessment = serializers.PrimaryKeyRelatedField(read_only=True)
    selected_option = serializers.PrimaryKeyRelatedField(
        queryset=QuestionOption.objects.all(),
        write_only=True,
        allow_null=True
    )

    class Meta:
        model = AssessmentAnswer
        fields = [
            'id',
            'assessment',
            'question',
            'answer',
            'selected_option',
            'index',
        ]