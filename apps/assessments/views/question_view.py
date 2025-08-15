from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.assessments.serializers.question_serializer import QuestionSerializer
from apps.assessments.services.question_service import QuestionService
from apps.assessments.schemas.question_schema import question_list_schema

class QuestionView(APIView):
    permission_classes = [IsAuthenticated]
    
    def __init__(self):
        self.service = QuestionService()
    
    @question_list_schema
    def get(self, request):
        
        try:
            questions = self.service.get_all()
            serializer = QuestionSerializer(questions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
