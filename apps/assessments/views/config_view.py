from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.assessments.schemas.question_schema import config_schema
from apps.assessments.serializers.question_serializer import QuestionSerializer
from apps.assessments.services.question_service import QuestionService


class ConfigView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self):
        self.service = QuestionService()

    @config_schema
    def get(self, request):
        try:
            questions = self.service.get_all()
            questions_serializer = QuestionSerializer(questions, many=True)

            server_time = timezone.now()

            return Response({
                "questions": questions_serializer.data,
                "server_time": server_time
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )