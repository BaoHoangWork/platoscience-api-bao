from django.core.mail import send_mail
from apps.users.models.user_model import User

class EmailService:
    def verify_email(self, email, code):
        try:
            user = User.objects.get(email=email)
            if not user:
                return False, "User with this email does not exist"
            if user.is_code_valid(code, False):
                user.is_verified = True
                user.verification_code_expires = None
                user.save()
                return True, "Email verified successfully"
            else:
                return False, "Invalid or expired verification code"
        except User.DoesNotExist:
            return False, "Invalid verification code"

    def send_verification_email(self, user):
        code = user.generate_code()
        subject = "Verify your email address"
        message = f"""
        Hi {user.first_name or 'User'},
        
        Please enter the following verification code to verify your email address:
        {code}
        
        This code will expire in 24 hours.
        
        If you didn't create an account, please ignore this email.
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email='noreply@rtech.live',
            recipient_list=[user.email],
            fail_silently=False,
        )

    def resend_verification_email(self, user):
        if not user.is_verified:
            self.send_verification_email(user)
            return True, "Verification email resent successfully"
        return False, "User is already verified"
    
    def send_forgot_password_email(self, user):
        try:
            code = user.generate_code(is_forgot_password=True)
            subject = "Reset your password"
            message = f"""
            Hi {user.first_name or 'User'},
            
            Please enter the following code to reset your password:
            {code}
            
            This code will expire in 15 minutes.
            
            If you didn't request a password reset, please ignore this email.
            """
            
            send_mail(
                subject=subject,
                message=message,
                from_email='Platoscience',
                recipient_list=[user.email],
                fail_silently=False,
            )
            return True, "Forgot password email sent successfully"
        except Exception as e:
            return False, f"Error sending forgot password email: {str(e)}"

    def verify_forgot_password_code(self, email, code):
        try:
            user = User.objects.filter(email=email).first()
            
            if not user:
                return False
            
            if user.is_code_valid(code, is_forgot_password=True) == True:
                return True
            else:
                return False
                
        except Exception as e:
            return False, f"Error verifying code: {str(e)}"
