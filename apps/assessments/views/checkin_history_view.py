from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.assessments.models import Assessment
from apps.assessments.serializers.checkin_history_serializer import CheckInHistoryDaySerializer, CheckInAnswerSerializer
from django.db.models.functions import TruncDate
from apps.assessments.schemas.check_in_schema import checkin_history_schema

class CheckInHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    @checkin_history_schema
    def get(self, request, assessment_id):
        assessment = Assessment.objects.filter(id=assessment_id, user=request.user).first()
        if not assessment:
            return Response({'error': 'Assessment not found or access denied'}, status=status.HTTP_404_NOT_FOUND)

        checkin_answers = assessment.answers.filter(is_checkin=True).annotate(checkin_day=TruncDate('checkin_date')).order_by('-checkin_date')
        history = {}
        for ans in checkin_answers:
            day = ans.checkin_day
            if day not in history:
                history[day] = []
            history[day].append(ans)

        result = []
        for day, answers in sorted(history.items(), reverse=True):
            result.append({
                'date': day,
                'answers': CheckInAnswerSerializer(answers, many=True).data
            })
        return Response({'checkin_history': result}, status=status.HTTP_200_OK)
