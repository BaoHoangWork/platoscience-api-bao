"""
URL configuration for plato_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from apps.assessments.views.assessment_view import AssessmentView
from apps.users.views.user_view import UserView, LoginView, LogoutView, UpdateUserPasswordView
from apps.users.views.email_view import VerifyEmailView, ResendVerificationView, ForgotPasswordView, VerifyForgotPasswordCodeView
from apps.assessments.views.assessment_view import AssessmentView, LatestAssessmentView, CheckTimeIntervalView
from apps.assessments.views.question_view import QuestionView, CheckInView, CheckInQuestionsView

api_patterns = [
    path('accounts/', UserView.as_view(), name='account'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('resend-verification/', ResendVerificationView.as_view(), name='resend-verification'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('verify-forgot-password-code/', VerifyForgotPasswordCodeView.as_view(), name='verify-forgot-password-code'),
    path('update-password/', UpdateUserPasswordView.as_view(), name='update-password'),
    path('assessments/', AssessmentView.as_view(), name='assessment'),
    path('assessments/latest/', LatestAssessmentView.as_view(), name='latest-assessment'),
    path('check-time-interval/', CheckTimeIntervalView.as_view(), name='check-time-interval'),
    path('questions/', QuestionView.as_view(), name='question'),
    path('check-in/', CheckInView.as_view(), name='checkin'),
    path('check-in-questions/', CheckInQuestionsView.as_view(), name='checkin-questions'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/', include(api_patterns)),
]
