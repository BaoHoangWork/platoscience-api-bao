from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from apps.assessments.serializers.assessment_serializer import (
    AssessmentSerializer,
    CreateAssessmentSerializer
)

assessment_list_schema = extend_schema(
    summary="List Assessments",
    description="Retrieve a list of assessments for the authenticated user.",
    responses={
        200: OpenApiResponse(
            description="List of assessments retrieved successfully",
            response=AssessmentSerializer(many=True),
            examples=[
                OpenApiExample(
                    "Success Response",
                    value=[
                        {
                            "id": 1,
                            "title": "Math Assessment",
                            "description": "An assessment on basic math skills.",
                            "created_at": "2023-10-01T12:00:00Z",
                            "phq_score": 12,
                            "bdi_score": 25,
                            "plato_score": 3.0,
                            "protocol": {
                                "intensity": "Medium",
                                "duration": "20 mins",
                                "node_placement": "Left Arm",
                                "node_type": "Type B",
                                "node_size": "Medium"
                            },
                            "severity": 1,
                            "answers": [
                                {
                                    "id": 1,
                                    "question": "What is 2 + 2?",
                                    "answer": "null",
                                    "selected_option": {
                                        "id": 1,
                                        "label": "test option",
                                        "value": "testttt"
                                    },
                                    "index": 0
                                },
                                {
                                    "id": 2,
                                    "question": "What is the capital of France?",
                                    "answer": "Paris",
                                    "index": 1
                                }
                            ]
                            
                        },
                        {
                            "id": 2,
                            "title": "Science Assessment",
                            "description": "An assessment on basic science concepts.",
                            "created_at": "2023-10-02T12:00:00Z",
                            "phq_score": 10,
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
                                    "id": 3,
                                    "question": "What is the chemical symbol for water?",
                                    "answer": "H2O",
                                    "index": 0
                                },
                                {
                                    "id": 4,
                                    "question": "What planet is known as the Red Planet?",
                                    "answer": "Mars",
                                    "index": 1
                                }
                            ]
                        }
                    ]
                )
            ]
        ),
        401: OpenApiResponse(description="Authentication required"),
        403: OpenApiResponse(description="Forbidden access")
    },
    tags=["Assessments"]
)

create_assessment_schema = extend_schema(
    summary="Create Assessment",
    description="Create a new assessment with answers.",
    request=CreateAssessmentSerializer(),
    examples=[
        OpenApiExample(
            'Example Request',
            value={
                "answers": [
                    {
                        "question": 5,
                        "answer": "answer 1",
                        "selected_option": 4,
                        "index": 0
                    },
                    {
                        "question": 9,
                        "answer": "answer 2",
                        "selected_option": 15,
                        "index": 3
                    },
                    {
                        "question": 10,
                        "answer": "answer 3",
                        "selected_option": 18,
                        "index": 3
                    },
                    {
                    "question": 11,
                    "answer": "The individual experiences persistent low mood, fatigue, and a lack of motivation. They report difficulty concentrating, disrupted sleep patterns, and irregular eating habits. Although still able to function in daily life, tasks feel overwhelmingly difficult and emotionally draining. There is significant social withdrawal, feelings of guilt, and recurring intrusive thoughts that contribute to a sense of hopelessness. Emotional numbness alternates with unpredictable episodes of sadness or anxiety. Despite outwardly appearing functional, the internal distress is constant and exhausting.",
                    "selected_option": None,
                    "index": 3
                    }
                ]
            },
            request_only=True,
        )
    ],
    responses={
        201: OpenApiResponse(
            description="Create a new assessment successfully",
            response=AssessmentSerializer(),
            examples=[
                OpenApiExample(
                    "Success Response",
                    value={
                        "status": "success",
                        "message": "Asessment created successfully",
                        "depression_type": "None",
                        "analysis": "The individual reports a constellation of symptoms including persistent low mood, fatigue, lack of motivation, difficulty concentrating, disrupted sleep, irregular eating habits, social withdrawal, feelings of guilt, recurring intrusive thoughts, hopelessness, emotional numbness, and unpredictable episodes of sadness or anxiety. These symptoms cause significant distress and make daily tasks feel overwhelmingly difficult and emotionally draining, although the individual is still able to function. The symptoms described do not clearly align with a specific duration, making it difficult to definitively diagnose Major Depressive Disorder (at least two weeks) or Persistent Depressive Disorder (at least two years in adults). Further questioning about the duration and specific triggers or causes is needed to differentiate between possible diagnoses.",
                        "assessment": {
                            "id": 252,
                            "phq_score": 4,
                            "bdi_score": 3,
                            "plato_score": 30.7,
                            "protocol": None,
                            "severity": 1,
                            "answers": [
                            {
                                "id": 486,
                                "assessment": 252,
                                "question": {
                                    "name": "bdi_q1",
                                    "content": "I do not feel sad / I feel sad / I am sad all the time",
                                    "description": "BDI Question 1",
                                    "category": "bdi",
                                    "options": [
                                        {
                                            "id": 2,
                                            "label": "Option A - Q5",
                                            "value": "1"
                                        },
                                        {
                                            "id": 3,
                                            "label": "Option B - Q5",
                                            "value": "2"
                                        },
                                        {
                                            "id": 4,
                                            "label": "Option C - Q5",
                                            "value": "3"
                                        }
                                    ],
                                    "type": "radio"
                                },
                                "answer": "answer 1",
                                "selected_option": {
                                    "id": 4,
                                    "label": "Option C - Q5",
                                    "value": "3"
                                },
                                "index": 0
                            },
                            {
                                "id": 487,
                                "assessment": 252,
                                "question": {
                                "name": "phq_q2",
                                "content": "Feeling down, depressed, or hopeless?",
                                "description": "PHQ Question 2",
                                "category": "phq",
                                "options": [
                                    {
                                        "id": 14,
                                        "label": "Option A - Q9",
                                        "value": "1"
                                    },
                                    {
                                        "id": 15,
                                        "label": "Option B - Q9",
                                        "value": "2"
                                    },
                                    {
                                        "id": 16,
                                        "label": "Option C - Q9",
                                        "value": "3"
                                    }
                                ],
                                "type": "radio"
                                },
                                "answer": "answer 2",
                                "selected_option": {
                                    "id": 15,
                                    "label": "Option B - Q9",
                                    "value": "2"
                                    },
                                "index": 3
                            },
                            {
                                "id": 488,
                                "assessment": 252,
                                "question": {
                                    "name": "phq_q3",
                                    "content": "Trouble falling or staying asleep?",
                                    "description": "PHQ Question 3",
                                    "category": "phq",
                                    "options": [
                                        {
                                        "id": 17,
                                        "label": "Option A - Q10",
                                        "value": "1"
                                        },
                                        {
                                        "id": 18,
                                        "label": "Option B - Q10",
                                        "value": "2"
                                        },
                                        {
                                        "id": 19,
                                        "label": "Option C - Q10",
                                        "value": "3"
                                        }
                                    ],
                                    "type": "checkbox"
                                },
                                "answer": "answer 3",
                                "selected_option": {
                                    "id": 18,
                                    "label": "Option B - Q10",
                                    "value": "2"
                                },
                                "index": 3
                            },
                            {
                                "id": 489,
                                "assessment": 252,
                                "question": {
                                    "name": "analytic 1",
                                    "content": "The individual experiences persistent low mood, fatigue, and a lack of motivation. They report difficulty concentrating, disrupted sleep patterns, and irregular eating habits. Although still able to function in daily life, tasks feel overwhelmingly difficult and emotionally draining. There is significant social withdrawal, feelings of guilt, and recurring intrusive thoughts that contribute to a sense of hopelessness. Emotional numbness alternates with unpredictable episodes of sadness or anxiety. Despite outwardly appearing functional, the internal distress is constant and exhausting.",
                                    "description": "The individual experiences persistent low mood, fatigue, and a lack of motivation. They report difficulty concentrating, disrupted sleep patterns, and irregular eating habits. Although still able to function in daily life, tasks feel overwhelmingly difficult and emotionally draining. There is significant social withdrawal, feelings of guilt, and recurring intrusive thoughts that contribute to a sense of hopelessness. Emotional numbness alternates with unpredictable episodes of sadness or anxiety. Despite outwardly appearing functional, the internal distress is constant and exhausting.",
                                    "category": "analytic",
                                    "options": [],
                                    "type": "text"
                                },
                                "answer": "The individual experiences persistent low mood, fatigue, and a lack of motivation. They report difficulty concentrating, disrupted sleep patterns, and irregular eating habits. Although still able to function in daily life, tasks feel overwhelmingly difficult and emotionally draining. There is significant social withdrawal, feelings of guilt, and recurring intrusive thoughts that contribute to a sense of hopelessness. Emotional numbness alternates with unpredictable episodes of sadness or anxiety. Despite outwardly appearing functional, the internal distress is constant and exhausting.",
                                "selected_option": None,
                                "index": 3
                            }
                            ],
                            "suggested_protocols": [],
                            "created_at": "2025-08-01T11:15:43.240486Z"
                        }
                    }
                )
            ]
        ),
        400: OpenApiResponse(description="BAD REQUEST"),
        401: OpenApiResponse(description="Authentication required"),
        403: OpenApiResponse(description="Must wait 4 weeks before creating a new assessment.")
    },
    tags=["Assessments"]
)

latest_assessment_schema = extend_schema(
    summary="Get latest assessment for profile",
    description="Retrieves the user's most recent assessment with suggested protocols and answers",
    tags=["Assessments"],
    responses={
        200: OpenApiResponse(
            description="Latest assessment with related data",
        ),
        401: OpenApiResponse(description="Authentication required"),
        404: OpenApiResponse(description="No assessment found"),
    },
)

select_protocol_schema = extend_schema(
    summary="Select Protocol from Suggested Protocols",
    description="Update the user's latest assessment with one of the suggested protocols.",
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'protocolId': {
                    'type': 'integer',
                    'description': 'ID of one of the suggested protocols to select'
                }
            },
            'required': ['protocolId']
        }
    },
    examples=[
        OpenApiExample(
            'Example Request',
            value={
                "protocolId": 2
            },
            request_only=True,
        )
    ],
    responses={
        200: OpenApiResponse(
            description="Protocol selected successfully",
            response=AssessmentSerializer(),
            examples=[
                OpenApiExample(
                    "Success Response",
                    value={
                        "id": 1,
                        "phq_score": 15,
                        "bdi_score": 30,
                        "plato_score": 3.5,
                        "protocol": {
                            "id": 2,
                            "intensity": "Medium",
                            "duration": "20 mins",
                            "node_placement": "Chest",
                            "node_type": "Type B",
                            "node_size": "Medium"
                        },
                        "severity": 2,
                        "answers": [],
                        "suggested_protocols": [
                            {
                                "id": 1,
                                "first_protocol": {
                                    "id": 1,
                                    "intensity": "High",
                                    "duration": "30 mins",
                                    "node_placement": "Head",
                                    "node_type": "Type A",
                                    "node_size": "Large"
                                },
                                "second_protocol": {
                                    "id": 2,
                                    "intensity": "Medium",
                                    "duration": "20 mins",
                                    "node_placement": "Chest",
                                    "node_type": "Type B",
                                    "node_size": "Medium"
                                },
                                "third_protocol": {
                                    "id": 3,
                                    "intensity": "Low",
                                    "duration": "15 mins",
                                    "node_placement": "Forehead",
                                    "node_type": "Type C",
                                    "node_size": "Small"
                                }
                            }
                        ],
                        "created_at": "2025-08-04T16:43:06.802369Z"
                    }
                )
            ]
        ),
        400: OpenApiResponse(
            description="Bad Request - protocolId is required or invalid protocol selection",
            examples=[
                OpenApiExample(
                    "Missing protocolId",
                    value={"error": "protocolId is required"}
                ),
                OpenApiExample(
                    "Invalid protocol selection",
                    value={
                        "error": "Invalid protocol selection. You can only choose from suggested protocols: [1, 2, 3]",
                        "valid_protocol_ids": [1, 2, 3]
                    }
                )
            ]
        ),
        404: OpenApiResponse(
            description="Not Found - No assessment or suggested protocols found",
            examples=[
                OpenApiExample(
                    "No assessment found",
                    value={"error": "No assessment found for user"}
                ),
                OpenApiExample(
                    "No suggested protocols",
                    value={"error": "No suggested protocols found for this assessment"}
                )
            ]
        ),
        401: OpenApiResponse(description="Authentication required"),
        500: OpenApiResponse(description="Internal server error")
    },
    tags=["Assessments"]
)