from apps.common.base_service import BaseService
from apps.users.models.user_model import User
from apps.users.repositories.user_repository import UserRepository
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction
from apps.users.services.email_service import EmailService

class UserService(BaseService):
    def __init__(self):
        super().__init__(UserRepository())

    def authenticate_user(self, email: str, password: str):
        user = self.repository.get_by_credentials(email, password)
        if not user:
            return None
        return user
    
    def create(self, **validated_data):
        try:
            with transaction.atomic():
                user = super().create(**validated_data)
                email_service = EmailService()
                email_service.send_verification_email(user)
                return user
        
        except Exception as e:
            raise Exception(f"Error creating user: {str(e)}")

    def generate_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        refresh['id'] = user.id
        refresh['email'] = user.email
        refresh['is_verified'] = user.is_verified
        refresh['is_staff'] = user.is_staff
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    
    def verify_email(self, code):
        try:
            user = User.objects.get(verification_code=code)
            if user.is_code_valid(code):
                user.is_verified = True
                user.verification_code_expires = None
                user.save()
                return True, "Email verified successfully"
            else:
                return False, "Invalid or expired verification code"
        except User.DoesNotExist:
            return False, "Invalid verification code"
        
    def get_by_email(self, email: str):
        return self.repository.get_by_email(email)
