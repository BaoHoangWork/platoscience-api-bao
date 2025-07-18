from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from apps.users.serializers.user_serializer import (
    UserSerializer, 
    LoginSerializer, 
    UpdatePasswordSerializer,
    ErrorResponseSerializer,
    SuccessMessageSerializer
)

user_create_schema = extend_schema(
    summary="Create new user",
    description="Create a new user user with email and password.",
    request=UserSerializer,
    responses={
        201: OpenApiResponse(
            description="User created successfully",
            response={
                "type": "object",
                "properties": {
                    "status": {"type": "string"},
                    "message": {"type": "string"},
                    "user": {
                        "type": "object",
                        "properties": {
                            "email": {"type": "string"},
                            "user_id": {"type": "int"}
                        }
                    }
                }
            },
            examples=[
                OpenApiExample(
                    "Success Response",
                    value={
                        "status": "success",
                        "message": "User created successfully",
                        "user": {
                            "email": "user@example.com",
                            "user_id": 1
                        }
                    }
                )
            ]
        ),
        400: OpenApiResponse(description="Validation error or User creation failed"),
    },
    tags=["Accounts"]
)

login_schema = extend_schema(
    summary="Login",
    description="Login to created account with email and password.",
    request=LoginSerializer,
    responses={
        200: OpenApiResponse(
            description="Login successful",
            response={
                "type": "object",
                "properties": {
                    "status": {"type": "string"},
                    "message": {"type": "string"},
                    "tokens": {
                        "type": "object",
                        "properties": {
                            "refresh": {"type": "string"},
                            "access": {"type": "string"}
                        }
                    }
                }
            },
            examples=[
                OpenApiExample(
                    "Success Response",
                    value={
                        "status": "success",
                        "message": "Login successful",
                        "tokens": {
                            'refresh': "REFRESH TOKEN",
                            'access': "ACCESS TOKEN",
                        }
                    }
                )
            ]
        ),
        400: OpenApiResponse(
            description="BAD REQUEST",
            response=ErrorResponseSerializer,
            examples=[
                OpenApiExample(
                    "Invalid inputs",
                    value={
                        "error": "Invalid inputs."
                    }
                )
            ]
        ),
        401: OpenApiResponse(
            description="Invalid credentials",
            response=ErrorResponseSerializer,
            examples=[
                OpenApiExample(
                    "Invalid credentials",
                    value={
                        "error": "Invalid credentials"
                    }
                )
            ]
        ),
        403: OpenApiResponse(
            description="Email not verified",
            response=ErrorResponseSerializer,
            examples=[
                OpenApiExample(
                    "Unverified email",
                    value={
                        "error": "Email not verified"
                    }
                )
            ]
        )
    },
    tags=["Accounts"]
)

logout_schema = extend_schema(
    summary="Log out",
    description="Log out.",
    responses={
        200: OpenApiResponse(
            description="Login successful",
            response={
                "type": "object",
                "properties": {
                    "status": {"type": "string"},
                    "message": {"type": "string"}
                }
            },
            examples=[
                OpenApiExample(
                    "Success Response",
                    value={
                        'status': 'success',
                        'message': 'Logout successful'
                    }
                )
            ]
        ),
        400: OpenApiResponse(
            description="BAD REQUEST",
            response=ErrorResponseSerializer,
            examples=[
                OpenApiExample("Failed to logout", value={'error': '...'}),
            ]
        )
    },
    tags=["Accounts"]
)

update_user_password_schema = extend_schema(
    summary="Update user password",
    description="Update password for user account.",
    request=UpdatePasswordSerializer,
    responses={
        200: OpenApiResponse(
            description="Login successful",
            response=SuccessMessageSerializer,
            examples=[
                OpenApiExample(
                    "Success Response",
                    value={
                        'message': 'Password updated successfully'
                    }
                )
            ]
        ),
        400: OpenApiResponse(
            description="Invalid data, or Failed to update password",
            response=ErrorResponseSerializer,
            examples=[
                OpenApiExample("Invalid data", value={'error': 'Invalid data', 'details': "..."}),
                OpenApiExample("Failed to update password", value={'error': 'Failed to update password'}),
                OpenApiExample("Error updating pwd", value={'error': f'Error updating password: ...'}),
            ]
        ),
        403: OpenApiResponse(
            description="Forgot password code is not verified.",
            response=ErrorResponseSerializer,
            examples=[
                OpenApiExample("Unverifed forgot pwd code", value={'error': 'user forgot password code is not verified'}),
            ]
        ),
        404: OpenApiResponse(
            description="User not found",
            response=ErrorResponseSerializer,
            examples=[
                OpenApiExample(
                    "Not found",
                    value={
                        'error': 'User not found'
                    }
                )
            ]
        ),
        403: OpenApiResponse(description="User forgot password code is not verified")
    },
    tags=["Accounts"]
)
