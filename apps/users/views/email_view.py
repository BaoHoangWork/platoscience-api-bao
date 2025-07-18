from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.users.services.email_service import EmailService
from apps.users.services.user_service import UserService
from apps.users.serializers.user_serializer import UpdatePasswordSerializer
from apps.users.views.user_view import UpdateUserPasswordView

from apps.users.schemas.email_schemas import verify_email_schema, resend_verification_schema, verify_forgot_pwd_code_schema, forgot_password_schema
class VerifyEmailView(APIView):

    @verify_email_schema
    def post(self, request):
        try:
            code = request.data.get('code')
            email = request.data.get('email')
            if not email:
                return Response(
                    {'error': 'Email is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if not code:
                return Response(
                    {'error': 'Code is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            success, message = EmailService().verify_email(email, code)
            if success:
                return Response(
                    {'message': message},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': message},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class ResendVerificationView(APIView):
    
    @resend_verification_schema
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = UserService().filter(email=email).first()

        user_service = UserService()

        if not user_service.authenticate_user(email, password):
            return Response(
                {'error': 'User is not authenticated'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        success, message = EmailService().resend_verification_email(user)
        if success:
            return Response(
                {'message': message},
                status=status.HTTP_200_OK
            )
        return Response(
            {'error': message},
            status=status.HTTP_400_BAD_REQUEST
        )

class ForgotPasswordView(APIView):

    @forgot_password_schema
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response(
                {'error': 'Email is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = UserService().filter(email=email).first()
        if not user:
            return Response(
                {'error': 'User with this email does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        success, message = EmailService().send_forgot_password_email(user)
        if success:
            return Response(
                {'message': message},
                status=status.HTTP_200_OK
            )
        return Response(
            {'error': message},
            status=status.HTTP_400_BAD_REQUEST
        )
    
class VerifyForgotPasswordCodeView(APIView):

    @verify_forgot_pwd_code_schema
    def post(self, request):
        try:
            data = request.data
            email = data.get('email')
            code = data.get('code')
            if not email or not code:
                return Response(
                    {'error': 'Email and code are required'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if EmailService().verify_forgot_password_code(email, code) is True:
                return Response(
                    {'message': 'Code verified successfully'},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': 'Invalid or expired code'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )