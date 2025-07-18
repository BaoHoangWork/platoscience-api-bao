from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from apps.users.models.user_model import User
from unittest.mock import patch
from datetime import timedelta
from django.utils import timezone
import json

class UserViewTestCase(APITestCase):
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpassword123',
            'first_name': 'Test',
            'last_name': 'User',
            'sex': 'male'
        }
        self.create_url = '/api/accounts/'
        self.login_url = '/api/auth/login/'
        self.logout_url = '/api/auth/logout/'
        self.verify_email_url = '/api/verify-email/'
        self.resend_verification_url = '/api/resend-verification/'
        
    def create_test_user(self, verified=False):
        """Helper method to create a test user"""
        user = User.objects.create(
            email=self.user_data['email'],
            password=self.user_data['password'],
            first_name=self.user_data['first_name'],
            last_name=self.user_data['last_name'],
            sex=self.user_data['sex'],
            is_verified=verified,
            verification_code='123456' if not verified else None,
            verification_code_expires=timezone.now() + timedelta(hours=1) if not verified else None
        )
        return user

    @patch('django.core.mail.send_mail')
    def test_create_user_success(self, mock_send_mail):
        """Test successful user creation"""
        mock_send_mail.return_value = True
        
        response = self.client.post(
            self.create_url,
            data=json.dumps(self.user_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['message'], 'User created successfully')
        self.assertEqual(response.data['user']['email'], self.user_data['email'])
        
        user = User.objects.get(email=self.user_data['email'])
        self.assertIsNotNone(user)
        self.assertFalse(user.is_verified)
        self.assertIsNotNone(user.verification_code)

    def test_create_user_invalid_data(self):
        """Test user creation with invalid data"""
        invalid_data = {
            'email': 'invalid-email',
            'password': '',
            'first_name': '',
            'last_name': '',
        }
        
        response = self.client.post(
            self.create_url,
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_create_user_duplicate_email_unverified(self):
        """Test creating user with existing unverified email"""
        self.create_test_user(verified=False)
        
        response = self.client.post(
            self.create_url,
            data=json.dumps(self.user_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertIn('Email already exists but not verified', response.data['error'])

    def test_login_success(self):
        """Test successful login with verified user"""
        user = self.create_test_user(verified=True)
        
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        
        with patch('apps.users.services.user_service.UserService.authenticate_user') as mock_auth:
            with patch('apps.users.services.user_service.UserService.generate_tokens') as mock_tokens:
                mock_auth.return_value = user
                mock_tokens.return_value = {'access': 'test_token', 'refresh': 'refresh_token'}
                
                response = self.client.post(
                    self.login_url,
                    data=json.dumps(login_data),
                    content_type='application/json'
                )
                
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(response.data['message'], 'Login successful')
                self.assertIn('tokens', response.data)

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        login_data = {
            'email': 'wrong@example.com',
            'password': 'wrongpassword'
        }
        
        with patch('apps.users.services.user_service.UserService.authenticate_user') as mock_auth:
            mock_auth.return_value = None
            
            response = self.client.post(
                self.login_url,
                data=json.dumps(login_data),
                content_type='application/json'
            )
            
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertIn('Invalid credentials', response.data['error'])

    def test_login_unverified_user(self):
        """Test login with unverified user"""
        user = self.create_test_user(verified=False)
        
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        
        with patch('apps.users.services.user_service.UserService.authenticate_user') as mock_auth:
            mock_auth.return_value = user
            
            response = self.client.post(
                self.login_url,
                data=json.dumps(login_data),
                content_type='application/json'
            )
            
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            self.assertIn('Email not verified', response.data['error'])

    def test_logout_success(self):
        """Test successful logout"""
        user = self.create_test_user(verified=True)

        self.client.force_authenticate(user=user)
        
        response = self.client.post(self.logout_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['message'], 'Logout successful')

    def test_logout_unauthenticated(self):
        """Test logout without authentication"""
        response = self.client.post(self.logout_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_verify_email_success(self):
        """Test successful email verification"""
        user = self.create_test_user(verified=False)
        
        verify_data = {
            'email': user.email,
            'code': user.verification_code
        }
        
        with patch('apps.users.services.email_service.EmailService.verify_email') as mock_verify:
            mock_verify.return_value = (True, 'Email verified successfully')
            
            response = self.client.post(
                self.verify_email_url,
                data=json.dumps(verify_data),
                content_type='application/json'
            )
            
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn('Email verified successfully', response.data['message'])

    def test_verify_email_invalid_code(self):
        """Test email verification with invalid code"""
        user = self.create_test_user(verified=False)
        
        verify_data = {
            'email': user.email,
            'code': 'invalid_code'
        }
        
        with patch('apps.users.services.email_service.EmailService.verify_email') as mock_verify:
            mock_verify.return_value = (False, 'Invalid or expired verification code')
            
            response = self.client.post(
                self.verify_email_url,
                data=json.dumps(verify_data),
                content_type='application/json'
            )
            
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn('Invalid or expired verification code', response.data['error'])

    def test_verify_email_missing_data(self):
        """Test email verification with missing data"""
        verify_data = {
            'email': 'test@example.com'
        }
        
        response = self.client.post(
            self.verify_email_url,
            data=json.dumps(verify_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Code is required', response.data['error'])

    def test_resend_verification_success(self):
        """Test successful resend verification email"""
        user = self.create_test_user(verified=False)
        
        resend_data = {
            'email': user.email,
            'password': self.user_data['password']
        }
        
        with patch('apps.users.services.user_service.UserService.authenticate_user') as mock_auth:
            with patch('apps.users.services.email_service.EmailService.resend_verification_email') as mock_resend:
                mock_auth.return_value = user
                mock_resend.return_value = (True, 'Verification email sent successfully')
                
                response = self.client.post(
                    self.resend_verification_url,
                    data=json.dumps(resend_data),
                    content_type='application/json'
                )
                
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertIn('Verification email sent successfully', response.data['message'])

    def test_resend_verification_invalid_credentials(self):
        """Test resend verification with invalid credentials"""
        user = self.create_test_user(verified=False)
        
        resend_data = {
            'email': user.email,
            'password': 'wrong_password'
        }
        
        with patch('apps.users.services.user_service.UserService.authenticate_user') as mock_auth:
            mock_auth.return_value = None
            
            response = self.client.post(
                self.resend_verification_url,
                data=json.dumps(resend_data),
                content_type='application/json'
            )
            
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertIn('User is not authenticated', response.data['error'])

    def test_resend_verification_service_failure(self):
        """Test resend verification when email service fails"""
        user = self.create_test_user(verified=False)
        
        resend_data = {
            'email': user.email,
            'password': self.user_data['password']
        }
        
        with patch('apps.users.services.user_service.UserService.authenticate_user') as mock_auth:
            with patch('apps.users.services.email_service.EmailService.resend_verification_email') as mock_resend:
                mock_auth.return_value = user
                mock_resend.return_value = (False, 'Failed to send email')
                
                response = self.client.post(
                    self.resend_verification_url,
                    data=json.dumps(resend_data),
                    content_type='application/json'
                )
                
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn('Failed to send email', response.data['error'])