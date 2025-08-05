from datetime import timedelta, timezone
from apps.assessments.serializers.assessment_answer_serializer import AssessmentAnswerSerializer
from apps.assessments.services.assessment_service import AssessmentService
from apps.assessments.serializers.assessment_serializer import AssessmentSerializer, CreateAssessmentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.assessments.schemas.assessment_schema import assessment_list_schema, latest_assessment_schema, create_assessment_schema, select_protocol_schema

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

class SelectProtocolView(APIView):
    permission_classes = [IsAuthenticated]
    
    def __init__(self):
        self.assessment_service = AssessmentService()
    
    @select_protocol_schema
    def post(self, request):
        try:
            protocol_id = request.data.get('protocolId')
            
            if not protocol_id:
                return Response(
                    {'error': 'protocolId is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            latest_assessment = self.assessment_service.get_latest_by_user(request.user)
            if not latest_assessment:
                return Response(
                    {'error': 'No assessment found for user'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            if not latest_assessment.suggested_protocols.exists():
                return Response(
                    {'error': 'No suggested protocols found for this assessment'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            suggested_protocol = latest_assessment.suggested_protocols.first()
            
            # Check if the provided protocol_id is one of the suggested protocols
            valid_protocol_ids = []
            selected_protocol = None
            
            if suggested_protocol.first_protocol and suggested_protocol.first_protocol.id == protocol_id:
                selected_protocol = suggested_protocol.first_protocol
            elif suggested_protocol.second_protocol and suggested_protocol.second_protocol.id == protocol_id:
                selected_protocol = suggested_protocol.second_protocol  
            elif suggested_protocol.third_protocol and suggested_protocol.third_protocol.id == protocol_id:
                selected_protocol = suggested_protocol.third_protocol
            
            if not selected_protocol:
                # Build list of valid protocol IDs for error message
                if suggested_protocol.first_protocol:
                    valid_protocol_ids.append(suggested_protocol.first_protocol.id)
                if suggested_protocol.second_protocol:
                    valid_protocol_ids.append(suggested_protocol.second_protocol.id)
                if suggested_protocol.third_protocol:
                    valid_protocol_ids.append(suggested_protocol.third_protocol.id)
                    
                return Response(
                    {
                        'error': f'Invalid protocol selection. You can only choose from suggested protocols: {valid_protocol_ids}',
                        'valid_protocol_ids': valid_protocol_ids
                    }, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            updated_assessment = self.assessment_service.update(
                latest_assessment.id, 
                protocol=selected_protocol
            )
            
            serializer = AssessmentSerializer(updated_assessment)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )