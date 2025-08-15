from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from apps.assessments.serializers.question_serializer import (QuestionSerializer)

question_list_schema = extend_schema(
    summary="List Questions",
    description="Retrieve a list of questions for the authenticated user.",
    responses={
        200: OpenApiResponse(
            description="List of questions retrieved successfully",
            response=QuestionSerializer(many=True),
            examples=[
                OpenApiExample(
                    "Success Response",
                    value=[
                        {
                            "id": 1,
                            "name": "BDI Question",
                            "content": "What is 2 + 2?",
                            "description": "A basic math question.",
                            "category": "phq",
                            "options": [
                                {"id":1, "label": "A", "value": "4"},
                                {"id":2, "label": "B", "value": "3"},
                                {"id":3, "label": "C", "value": "5"}
                            ],
                            "type": "radio"
                        },
                        {
                            "id": 2,
                            "name": "PHQ Question",
                            "content": "What is the chemical symbol for water?",
                            "description": "A basic science question.",
                            "category": "phq",
                            "options": [
                                {"id":1, "label": "A", "value": "H2O"},
                                {"id":2, "label": "B", "value": "CO2"},
                                {"id":3, "label": "C", "value": "O2"}
                            ],
                            "type": "select"
                        }
                    ]
                )
            ]
        )
    }
)

config_schema = extend_schema(
    summary="Get Configuration",
    description="Retrieve all questions and current server time for application configuration.",
    responses={
        200: OpenApiResponse(
            description="Configuration data retrieved successfully",
            examples=[
                OpenApiExample(
                    "Success Response",
                    value={
                        "questions": [
                            {
                                "name": "phq_q1",
                                "content": "Little interest or pleasure in doing things?",
                                "description": "PHQ Question 1",
                                "category": "phq",
                                "options": [
                                    {"id": 1, "label": "Not at all", "value": "0"},
                                    {"id": 2, "label": "Several days", "value": "1"},
                                    {"id": 3, "label": "More than half the days", "value": "2"},
                                    {"id": 4, "label": "Nearly every day", "value": "3"}
                                ],
                                "type": "radio"
                            },
                            {
                                "name": "bdi_q1",
                                "content": "I do not feel sad / I feel sad / I am sad all the time",
                                "description": "BDI Question 1",
                                "category": "bdi",
                                "options": [
                                    {"id": 5, "label": "I do not feel sad", "value": "0"},
                                    {"id": 6, "label": "I feel sad", "value": "1"},
                                    {"id": 7, "label": "I am sad all the time", "value": "2"}
                                ],
                                "type": "radio"
                            }
                        ],
                        "server_time": "2025-08-05T14:30:00.000Z"
                    }
                )
            ]
        ),
        401: OpenApiResponse(description="Authentication required"),
        500: OpenApiResponse(description="Server error")
    },
)