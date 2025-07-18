from rest_framework import serializers
from apps.assessments.models import Protocol

class ProtocolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Protocol
        fields = [
            'id',
            'intensity', 
            'duration',
            'node_placement',
            'node_type',
            'node_size'
        ]