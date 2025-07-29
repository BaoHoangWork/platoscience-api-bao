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
