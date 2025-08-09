from rest_framework import serializers
from apps.users.models import UserHealthData
from django.utils.dateparse import parse_datetime
from datetime import timedelta

class SleepDataSerializer(serializers.Serializer):
    start = serializers.CharField(help_text="Sleep start datetime in ISO format")
    end = serializers.CharField(help_text="Sleep end datetime in ISO format")

class UserHealthDataSerializer(serializers.ModelSerializer):
    sleep = SleepDataSerializer(write_only=True)
    
    class Meta:
        model = UserHealthData
        fields = ['sleep', 'steps', 'weight']
        
    def validate_sleep(self, value):
        try:
            start_datetime = parse_datetime(value['start'])
            end_datetime = parse_datetime(value['end'])
            
            if not start_datetime or not end_datetime:
                raise serializers.ValidationError("Invalid datetime format. Use ISO format.")
            
            if start_datetime >= end_datetime:
                raise serializers.ValidationError("Sleep start time must be before end time.")
                
            return value
        except Exception as e:
            raise serializers.ValidationError(f"Invalid sleep data: {str(e)}")

    def create(self, validated_data):
        sleep_data = validated_data.pop('sleep')
        user = self.context['request'].user  
        
        start_datetime = parse_datetime(sleep_data['start'])
        end_datetime = parse_datetime(sleep_data['end'])
        
        calculated_duration = end_datetime - start_datetime
        
        health_data = UserHealthData.objects.create(
            user=user,
            sleep_start_datetime=start_datetime,
            sleep_end_datetime=end_datetime,
            sleep_duration=calculated_duration,
            steps=validated_data['steps'],
            weight=validated_data['weight'],
            data_start_datetime=start_datetime,
            data_end_datetime=end_datetime
        )
        
        return health_data

class UserHealthDataResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserHealthData
        fields = ['id', 'sleep_start_datetime', 'sleep_end_datetime', 'sleep_duration', 'steps', 'weight', 'data_start_datetime', 'data_end_datetime']