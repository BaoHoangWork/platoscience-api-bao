from apps.assessments.models import SuggestedProtocol, Protocol
from rest_framework import serializers
from apps.assessments.serializers.protocol_serializer import ProtocolSerializer

class SuggestedProtocolSerializer(serializers.ModelSerializer):
    first_protocol = serializers.PrimaryKeyRelatedField(queryset=Protocol.objects.all(), allow_null=True, required=False)
    second_protocol = serializers.PrimaryKeyRelatedField(queryset=Protocol.objects.all(), allow_null=True, required=False)
    third_protocol = serializers.PrimaryKeyRelatedField(queryset=Protocol.objects.all(), allow_null=True, required=False)

    class Meta:
        model = SuggestedProtocol
        fields = [
            'id',
            'first_protocol',
            'second_protocol',
            'third_protocol'
        ]

class SuggestedProtocolDetailSerializer(serializers.ModelSerializer):
    first_protocol = ProtocolSerializer(read_only=True)
    second_protocol = ProtocolSerializer(read_only=True)
    third_protocol = ProtocolSerializer(read_only=True)

    class Meta:
        model = SuggestedProtocol
        fields = [
            'id',
            'first_protocol',
            'second_protocol',
            'third_protocol'
        ]