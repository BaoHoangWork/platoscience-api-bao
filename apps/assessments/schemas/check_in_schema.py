from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from apps.assessments.serializers.question_serializer import QuestionSerializer
from apps.users.serializers.user_serializer import ErrorResponseSerializer

checkin_history_schema = extend_schema(
    summary="Get Check-in History",
    description="Retrieve all check-in answers for an assessment, grouped by check-in date.",
    responses={
        200: OpenApiResponse(
            description="Check-in history grouped by date",
            response={
                "type": "object",
                "properties": {
                    "checkin_history": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "date": {"type": "string", "format": "date"},
                                "answers": {"type": "array", "items": {"$ref": "#/components/schemas/CheckInAnswer"}}
                            }
                        }
                    }
                }
            },
            examples=[
                OpenApiExample(
                    "Success Response",
                    value={
                        "checkin_history": [
                            {
                                "date": "2025-08-08",
                                "answers": [
                                    {
                                        "id": 1,
                                        "question": {
                                            "id": 4,
                                            "name": "daily_mood",
                                            "content": "How are you feeling today?",
                                            "description": "Daily mood check-in",
                                            "category": "checkin",
                                            "options": [
                                                {"id": 6, "label": "Very Good", "value": "5"},
                                                {"id": 7, "label": "Good", "value": "4"},
                                                {"id": 8, "label": "Neutral", "value": "3"},
                                                {"id": 9, "label": "Bad", "value": "2"},
                                                {"id": 10, "label": "Very Bad", "value": "1"}
                                            ],
                                            "type": "radio"
                                        },
                                        "answer": None,
                                        "selected_option": {"id": 8, "label": "Neutral", "value": "3"},
                                        "index": 0
                                    },
                                    {
                                        "id": 2,
                                        "question": {
                                            "id": 8,
                                            "name": "additional_notes",
                                            "content": "Any additional thoughts or notes for today?",
                                            "description": "Free text for additional thoughts",
                                            "category": "checkin",
                                            "options": [],
                                            "type": "text"
                                        },
                                        "answer": "Feeling okay today, a bit tired but overall fine.",
                                        "selected_option": None,
                                        "index": 4
                                    }
                                ]
                            },
                            {
                                "date": "2025-08-07",
                                "answers": [
                                    {
                                        "id": 3,
                                        "question": {
                                            "id": 4,
                                            "name": "daily_mood",
                                            "content": "How are you feeling today?",
                                            "description": "Daily mood check-in",
                                            "category": "checkin",
                                            "options": [
                                                {"id": 6, "label": "Very Good", "value": "5"},
                                                {"id": 7, "label": "Good", "value": "4"},
                                                {"id": 8, "label": "Neutral", "value": "3"},
                                                {"id": 9, "label": "Bad", "value": "2"},
                                                {"id": 10, "label": "Very Bad", "value": "1"}
                                            ],
                                            "type": "radio"
                                        },
                                        "answer": None,
                                        "selected_option": {"id": 7, "label": "Good", "value": "4"},
                                        "index": 0
                                    }
                                ]
                            }
                        ]
                    }
                )
            ]
        ),
        404: OpenApiResponse(description="Assessment not found or access denied"),
        401: OpenApiResponse(description="Authentication required"),
    },
    tags=["Check-in"]
)

checkin_questions_schema = extend_schema(
    summary="Get Check-in Questions",
    description="Retrieve all questions with category 'checkin' for daily check-ins.",
    responses={
        200: OpenApiResponse(
            description="Check-in questions retrieved successfully",
            response=QuestionSerializer(many=True),
            examples=[
                OpenApiExample(
                    "Success Response",
                    value=[
                        {
                            "id": 1,
                            "name": "daily_mood",
                            "content": "How are you feeling today?",
                            "description": "Daily mood check-in",
                            "category": "checkin",
                            "options": [
                                {"id": 1, "label": "Very Good", "value": "5"},
                                {"id": 2, "label": "Good", "value": "4"},
                                {"id": 3, "label": "Neutral", "value": "3"},
                                {"id": 4, "label": "Bad", "value": "2"},
                                {"id": 5, "label": "Very Bad", "value": "1"}
                            ],
                            "type": "radio"
                        },
                        {
                            "id": 2,
                            "name": "sleep_quality",
                            "content": "How was your sleep last night?",
                            "description": "Sleep quality assessment",
                            "category": "checkin",
                            "options": [
                                {"id": 6, "label": "Excellent", "value": "4"},
                                {"id": 7, "label": "Good", "value": "3"},
                                {"id": 8, "label": "Fair", "value": "2"},
                                {"id": 9, "label": "Poor", "value": "1"}
                            ],
                            "type": "radio"
                        },
                        {
                            "id": 3,
                            "name": "additional_notes",
                            "content": "Any additional thoughts or notes for today?",
                            "description": "Free text for additional thoughts",
                            "category": "checkin",
                            "options": [],
                            "type": "text"
                        }
                    ]
                )
            ]
        ),
        401: OpenApiResponse(description="Authentication required"),
        500: OpenApiResponse(
            description="Server error",
            response=ErrorResponseSerializer,
            examples=[
                OpenApiExample(
                    "Server Error",
                    value={"error": "Internal server error"}
                )
            ]
        )
    },
    tags=["Check-in"]
)

checkin_submit_schema = extend_schema(
    summary="Submit Check-in Answers",
    description="Submit daily check-in answers for an existing assessment.",
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "assessmentId": {
                    "type": "integer", 
                    "description": "ID of the assessment to attach check-in to",
                    "example": 123
                },
                "answers": {
                    "type": "array",
                    "description": "Array of check-in answers",
                    "items": {
                        "type": "object",
                        "properties": {
                            "question_id": {
                                "type": "integer", 
                                "description": "ID of the check-in question",
                                "example": 1
                            },
                            "answer": {
                                "type": "string", 
                                "description": "Text answer (for text type questions)", 
                                "nullable": True,
                                "example": "I feel good today"
                            },
                            "selected_option": {
                                "type": "integer", 
                                "description": "ID of selected option (for radio/select questions)", 
                                "nullable": True,
                                "example": 3
                            }
                        },
                        "required": ["question_id"],
                        "additionalProperties": False
                    }
                }
            },
            "required": ["assessmentId", "answers"],
            "additionalProperties": False
        }
    },
    examples=[
        OpenApiExample(
            "Check-in Submission",
            description="Example check-in submission with mixed question types",
            value={
                "assessmentId": 123,
                "answers": [
                    {
                        "question_id": 1,
                        "answer": None,
                        "selected_option": 3
                    },
                    {
                        "question_id": 2,
                        "answer": None,
                        "selected_option": 7
                    },
                    {
                        "question_id": 3,
                        "answer": "Had a good day today, feeling more positive than yesterday.",
                        "selected_option": None
                    }
                ]
            }
        )
    ],
    responses={
        200: OpenApiResponse(
            description="Check-in answers submitted successfully",
            response={
                "type": "object",
                "properties": {
                    "message": {"type": "string"},
                    "assessment": {"$ref": "#/components/schemas/Assessment"}
                }
            },
            examples=[
                OpenApiExample(
                    "Success Response",
                    description="Successful check-in submission with updated assessment",
                    value={
                        "message": "Successfully created 3 check-in answers",
                        "assessment": {
                            "id": 123,
                            "user": 1,
                            "phq_score": 12,
                            "bdi_score": 20,
                            "plato_score": 2.5,
                            "protocol": {
                                "intensity": "Low",
                                "duration": "15 mins",
                                "node_placement": "Right Arm",
                                "node_type": "Type A",
                                "node_size": "Small"
                            },
                            "severity": 0,
                            "answers": [
                                {
                                    "id": 501,
                                    "assessment": 123,
                                    "question": {
                                        "id": 1,
                                        "name": "daily_mood",
                                        "content": "How are you feeling today?",
                                        "description": "Daily mood check-in",
                                        "category": "checkin",
                                        "type": "radio"
                                    },
                                    "answer": None,
                                    "selected_option": {
                                        "id": 3,
                                        "label": "Neutral",
                                        "value": "3"
                                    },
                                    "index": 0,
                                    "is_checkin": True,
                                    "checkin_date": "2025-08-05T14:30:00Z"
                                },
                                {
                                    "id": 502,
                                    "assessment": 123,
                                    "question": {
                                        "id": 3,
                                        "name": "additional_notes",
                                        "content": "Any additional thoughts or notes for today?",
                                        "description": "Free text for additional thoughts",
                                        "category": "checkin",
                                        "type": "text"
                                    },
                                    "answer": "Had a good day today, feeling more positive than yesterday.",
                                    "selected_option": None,
                                    "index": 2,
                                    "is_checkin": True,
                                    "checkin_date": "2025-08-05T14:30:00Z"
                                }
                            ],
                            "created_at": "2025-08-01T11:15:43.240486Z"
                        }
                    }
                )
            ]
        ),
        400: OpenApiResponse(
            description="Bad request - validation errors",
            response=ErrorResponseSerializer,
            examples=[
                OpenApiExample(
                    "Missing question_id",
                    value={"error": "question_id is required for each answer"}
                ),
                OpenApiExample(
                    "Invalid question",
                    value={"error": "Question 999 is not a check-in question"}
                ),
                OpenApiExample(
                    "Missing answer data",
                    value={"error": "Either answer text or selected_option is required for question 1"}
                ),
                OpenApiExample(
                    "Invalid option",
                    value={"error": "Selected option with id 999 not found"}
                )
            ]
        ),
        401: OpenApiResponse(description="Authentication required"),
        404: OpenApiResponse(
            description="Assessment not found or access denied",
            response=ErrorResponseSerializer,
            examples=[
                OpenApiExample(
                    "Assessment not found",
                    value={"error": "Assessment not found or access denied"}
                ),
                OpenApiExample(
                    "Question not found",
                    value={"error": "Question with id 999 not found"}
                )
            ]
        )
    },
    tags=["Check-in"]
)