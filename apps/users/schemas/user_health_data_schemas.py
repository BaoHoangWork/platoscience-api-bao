from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from apps.users.serializers.user_health_data_serializer import UserHealthDataSerializer, UserHealthDataResponseSerializer
from apps.users.serializers.user_serializer import SuccessMessageSerializer, ErrorResponseSerializer

upload_health_data_schema = extend_schema(
    summary="Upload Health Data",
    description="Upload user health data including sleep information, steps, and weight.",
    request=UserHealthDataSerializer,
    examples=[
        OpenApiExample(
            'Example Request',
            value={
                "sleep": {
                    "duration": 480,
                    "start": "2025-08-05T22:00:00Z",
                    "end": "2025-08-06T06:00:00Z"
                },
                "steps": 8500,
                "weight": 70.5
            },
            request_only=True,
        )
    ],
    responses={
        201: OpenApiResponse(
            description="Health data uploaded successfully",
            response={
                "type": "object",
                "properties": {
                    "message": {"type": "string"},
                    "data": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "sleep_start_datetime": {"type": "string"},
                            "sleep_end_datetime": {"type": "string"},
                            "sleep_duration": {"type": "string"},
                            "steps": {"type": "integer"},
                            "weight": {"type": "number"},
                            "data_start_datetime": {"type": "string"},
                            "data_end_datetime": {"type": "string"}
                        }
                    }
                }
            },
            examples=[
                OpenApiExample(
                    "Success Response",
                    value={
                        "message": "Health data uploaded successfully",
                        "data": {
                            "id": 1,
                            "sleep_start_datetime": "2025-08-05T22:00:00Z",
                            "sleep_end_datetime": "2025-08-06T06:00:00Z",
                            "sleep_duration": "8:00:00",
                            "steps": 8500,
                            "weight": 70.5,
                            "data_start_datetime": "2025-08-05T22:00:00Z",
                            "data_end_datetime": "2025-08-06T06:00:00Z"
                        }
                    }
                )
            ]
        ),
        400: OpenApiResponse(
            description="Bad request - Invalid data",
            response=ErrorResponseSerializer,
            examples=[
                OpenApiExample(
                    "Invalid data",
                    value={
                        "error": "Invalid data",
                        "details": {
                            "sleep": ["Invalid datetime format. Use ISO format."],
                            "steps": ["This field is required."],
                            "weight": ["This field is required."]
                        }
                    }
                ),
                OpenApiExample(
                    "Invalid sleep time",
                    value={
                        "error": "Invalid data",
                        "details": {
                            "sleep": ["Sleep start time must be before end time."]
                        }
                    }
                ),
                OpenApiExample(
                    "Error uploading",
                    value={
                        "error": "Error uploading health data: ..."
                    }
                )
            ]
        ),
        401: OpenApiResponse(
            description="Authentication required",
            response=ErrorResponseSerializer,
            examples=[
                OpenApiExample(
                    "Unauthorized",
                    value={
                        "error": "Authentication required"
                    }
                )
            ]
        )
    },
)