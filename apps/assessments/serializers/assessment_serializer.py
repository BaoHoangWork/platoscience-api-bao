from rest_framework import serializers
from apps.assessments.models import Assessment
from apps.assessments.serializers.assessment_answer_serializer import AssessmentAnswerSerializer, CreateAssessmentAnswerSerializer
from apps.assessments.serializers.suggested_protocol_serializer import SuggestedProtocolDetailSerializer

class AssessmentSerializer(serializers.ModelSerializer):
    answers = AssessmentAnswerSerializer(many=True)
    suggested_protocols = SuggestedProtocolDetailSerializer(many=True)

    class Meta:
        model = Assessment
        fields = [
            'id',
            'phq_score',
            'bdi_score',
            'plato_score',
            'protocol',
            'severity',
            'answers',
            'suggested_protocols',
            'protocol_selected_date',
            'stopped_date',
            'stop_reason',
            'created_at',
        ]
        

class CreateAssessmentSerializer(serializers.ModelSerializer):
    answers = CreateAssessmentAnswerSerializer(many=True)

    class Meta:
        model = Assessment
        fields = [
            'id',
            'answers',
            'created_at',
        ]

