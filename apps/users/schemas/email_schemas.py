from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from apps.users.serializers.user_serializer import (
    LoginSerializer, 
    VerifyEmailSerializer, 
    EmailOnlySerializer, 
    SuccessMessageSerializer, 
    ErrorResponseSerializer
)

verify_email_schema = extend_schema(
    summary="Verify email",
    description="Verify email by sending the token.",
    request=VerifyEmailSerializer,
    responses={
        200: OpenApiResponse(
            description="Verify successfully.",
            response=SuccessMessageSerializer,
            examples=[
                OpenApiExample(
                    "Success Response",
                    value={
                        "message": "Email verified successfully",
                    }
                )
            ]
        ),
        400: OpenApiResponse(
            description="Missing or invalid email/code",
            response=ErrorResponseSerializer,
            examples=[
                OpenApiExample(
                    "Missing Fields",
                    value={"error": "Email/Code is required"}
                ),
                OpenApiExample(
                    "Invalid Code",
                    value={"error": "Invalid or expired verification token"}
                )
            ]
        ),
        500: OpenApiResponse(description="Server error"),
    },
    tags=["Emails"]
)

resend_verification_schema = extend_schema(
    summary="Resend verification",
    description="Resend verification to user.",
    request=LoginSerializer,
    responses={
        200: OpenApiResponse(
            description="Verify successfully.",
            response=SuccessMessageSerializer,
            examples=[
                OpenApiExample(
                    "Success Response",
                    value={
                        "message": "Verification email resent successfully",
                    }
                )
            ]
        ),
        400: OpenApiResponse(
            description="Bad request.",
            response=ErrorResponseSerializer,
            examples=[
                OpenApiExample(
                    "Failed to resend verification.",
                    value={
                        "error": "Failed to resend verification.",
                    }
                )
            ]
        ),
        401: OpenApiResponse(
            description="Unauthorized user",
            response=ErrorResponseSerializer,
            examples=[
                OpenApiExample(
                    "Unauthorized",
                    value={
                        "error": "User is not authenticated",
                    }
                )
            ]
        )
    },
    tags=["Emails"]
)

forgot_password_schema = extend_schema(
    summary="Forgot password",
    description="Send forgot password mail with code to user.",
    request=EmailOnlySerializer,
    responses={
        200: OpenApiResponse(
            description="Send forgot password email successfully.",
        ),
        400: OpenApiResponse(
            description='Bad Request or Missing email.', 
            response=ErrorResponseSerializer,
            examples=[
                OpenApiExample(
                    "Missing email",
                    value={
                        "error": "Email is required",
                    }
                )
            ]
        ),
        404: OpenApiResponse(
            description="Not found user.",
            response=ErrorResponseSerializer,
            examples=[
                OpenApiExample(
                    "Not found user",
                    value={
                        "error": "User with this email does not exist",
                    }
                )
            ]
        )
    },
    tags=["Emails"]
)

verify_forgot_pwd_code_schema = extend_schema(
    summary="Verify forgot password code",
    description="Verify forgot password code.",
    request=VerifyEmailSerializer,
    responses={
        200: OpenApiResponse(
            description="Code verified successfully.",
            response=SuccessMessageSerializer,
            examples=[
                OpenApiExample(
                    "Success response",
                    value={
                        "message": "Code verified successfully",
                    }
                )
            ]
        ),
        400: OpenApiResponse(
            description='Missing email/code or Invalid/expired code', 
            response=ErrorResponseSerializer,
            examples=[
                OpenApiExample(
                    "Missing email/code",
                    value={
                        "error": "Email and code are required",
                    }
                ),
                OpenApiExample(
                    "Invalid/expired code",
                    value={ 
                        'error': 'Invalid or expired code'
                    }
                )
            ]
        ),
        500: OpenApiResponse(
            description="Server error",
        )
    },
    tags=["Emails"]
)

