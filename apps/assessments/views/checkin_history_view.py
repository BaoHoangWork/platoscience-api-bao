from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.assessments.models import Assessment
from apps.assessments.services.assessment_service import AssessmentService
from apps.assessments.services.assessment_answer_service import AssessmentAnswerService
from apps.assessments.serializers.checkin_history_serializer import CheckInHistoryDaySerializer, CheckInAnswerSerializer
from django.db.models.functions import TruncDate
from apps.assessments.schemas.check_in_schema import checkin_history_schema

class CheckInHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self):
        self.assessment_service = AssessmentService()
        self.assessment_answer_service = AssessmentAnswerService()

    @checkin_history_schema
    def get(self, request, assessment_id):
        assessment = self.assessment_service.get_by_id(assessment_id)
        if not assessment or assessment.user != request.user:
            return Response({'error': 'Assessment not found or access denied'}, status=status.HTTP_404_NOT_FOUND)

        history = self.assessment_answer_service.get_checkin_history(assessment)
        serializer = CheckInHistoryDaySerializer(history, many=True)
        return Response({'checkin_history': serializer.data}, status=status.HTTP_200_OK)
