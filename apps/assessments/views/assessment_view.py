from datetime import timedelta, timezone
from apps.assessments.serializers.assessment_answer_serializer import AssessmentAnswerSerializer
from apps.assessments.services.assessment_service import AssessmentService
from apps.assessments.serializers.assessment_serializer import AssessmentSerializer, CreateAssessmentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.assessments.schemas.assessment_schema import assessment_list_schema, latest_assessment_schema, create_assessment_schema, stop_assessment_schema

class AssessmentView(APIView):
    def __init__(self):
        self.service = AssessmentService()

    def get_permissions(self):
        if self.request.method == "POST" or "PUT" or "DELETE":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    @assessment_list_schema
    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        assessments = self.service.get_all_by_user(user)
        serializer = AssessmentSerializer(assessments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @create_assessment_schema
    def post(self, request):
        check = self.service.is_valid_time(request.user)
        if not check["is_valid"]:
            return Response(
                {
                    'error': 'You can only create a new assessment after 4 weeks from the last one.',
                    "next_valid_time": check['next_valid_time']
                },
                status=status.HTTP_403_FORBIDDEN
            )

        assessment_serializer = CreateAssessmentSerializer(data=request.data)

        if assessment_serializer.is_valid():
            try:
                assessment = AssessmentService().create_with_answer(
                    assessment_data=assessment_serializer.validated_data,
                    user=request.user
                )

                return Response(
                    {
                        'status': 'success',
                        'message': 'Asessment created successfully',
                        "depression_type": assessment["depression_type"],
                        "analysis": assessment["analysis"],
                        'assessment': AssessmentSerializer(assessment["assessment"]).data,
                    }, 
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {
                    "errors": {
                        "assessment": assessment_serializer.errors,
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        

class CheckTimeIntervalView(APIView):
    def __init__(self):
        self.service = AssessmentService()

    def get_permissions(self):
        if self.request.method == "POST" or "PUT" or "DELETE":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    def post(self, request):
        check = self.service.is_valid_time(request.user)
        return Response(
            {
                "is_valid": check['is_valid'],
                "next_valid_time": check['next_valid_time']
            },
            status=status.HTTP_200_OK if check['is_valid'] else status.HTTP_403_FORBIDDEN
        )

class LatestAssessmentView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self):
        self.service = AssessmentService()

    @latest_assessment_schema
    def get(self, request):
        try:
            user = request.user
            latest_assessment = self.service.get_latest_by_user(user)

            if not latest_assessment:
                return Response({'error': 'No assessment found'}, status=status.HTTP_404_NOT_FOUND)

            serializer = AssessmentSerializer(latest_assessment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class AssessmentStopView(APIView):
    
    def __init__(self):
        self.service = AssessmentService()
        
    @stop_assessment_schema
    def post(self, request):
        try:
            user = request.user

            reason = request.data.get('reason')
            if reason is None:
                return Response(          
                    {'error': 'reason is not provided'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            res = self.service.end_assessment(user, reason)
            serializer = AssessmentSerializer(res)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(          
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )