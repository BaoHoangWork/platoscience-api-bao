from rest_framework import serializers
from apps.users.models.user_model import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'dob', 'sex']
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
class UpdatePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(min_length=8, write_only=True)
    
    class Meta:
        fields = ['email', 'new_password']

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()

class EmailOnlySerializer(serializers.Serializer):
    email = serializers.EmailField()

class ErrorResponseSerializer(serializers.Serializer):
    error = serializers.CharField()

class SuccessMessageSerializer(serializers.Serializer):
    message = serializers.CharField()
