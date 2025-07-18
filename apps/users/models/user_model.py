from django.db import models
import uuid
from django.utils import timezone
from datetime import timedelta
import random
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_staff = models.BooleanField(default=False)
    email = models.EmailField(unique=True, blank=True)
    is_verified = models.BooleanField(default=False)
    password = models.CharField(max_length=128)
    dob = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=10, null=True, blank=True)

    verification_code = models.CharField(max_length=6, null=True, blank=True)
    verification_code_expires = models.DateTimeField(null=True, blank=True)
    forgot_password_code = models.CharField(max_length=6, null=True, blank=True)
    forgot_password_code_expires = models.DateTimeField(null=True, blank=True)
    forgot_password_code_verified_at = models.DateTimeField(null=True, blank=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def generate_code(self, is_forgot_password=False):
        if is_forgot_password:
            self.forgot_password_code = str(random.randint(100000, 999999))
            self.forgot_password_code_expires = timezone.now() + timedelta(minutes=15)
            self.forgot_password_code_verified_at = None
            self.save()
            return self.forgot_password_code
        else: 
            self.verification_code = str(random.randint(100000, 999999))
            self.verification_code_expires = timezone.now() + timedelta(hours=24)
            self.save()
            return self.verification_code
    
    def is_code_valid(self, code, is_forgot_password):
        if is_forgot_password:
            if not str(self.forgot_password_code) == str(code):
                return False
            else:       
                self.forgot_password_code_verified_at = timezone.now()
                self.save()
                return (
                    str(self.forgot_password_code) == str(code) and
                    self.forgot_password_code_expires and
                    timezone.now() < self.forgot_password_code_expires
                )
        else:
            return (
                str(self.verification_code) == str(code) and
                self.verification_code_expires and
                timezone.now() < self.verification_code_expires
            )

    @property
    def is_authenticated(self):
        """Always return True for authenticated users"""
        return True
    
    @property
    def is_anonymous(self):
        """Always return False for users (opposite of is_authenticated)"""
        return False
    
    def __str__(self):
        return self.email
