from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.assessments.serializers.question_serializer import QuestionSerializer
from apps.assessments.services.question_service import QuestionService
from apps.assessments.schemas.check_in_schema import checkin_questions_schema, checkin_submit_schema
from apps.assessments.schemas.question_schema import question_list_schema
from apps.assessments.services.assessment_service import AssessmentService
from apps.assessments.services.assessment_answer_service import AssessmentAnswerService
from apps.assessments.services.question_option_service import QuestionOptionService
from django.utils import timezone

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
        
class CheckInQuestionsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def __init__(self):
        self.question_service = QuestionService()
    
    @checkin_questions_schema
    def get(self, request):
        try:
            questions = self.question_service.filter(category='checkin')
            serializer = QuestionSerializer(questions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CheckInView(APIView):
    permission_classes = [IsAuthenticated]
    
    def __init__(self):
        self.assessment_service = AssessmentService()
        self.assessment_answer_service = AssessmentAnswerService()
        self.question_service = QuestionService()
        self.question_option_service = QuestionOptionService()
    
    @checkin_submit_schema
    def post(self, request):
        try:
            assessment_id = request.data.get('assessmentId')
            answers_data = request.data.get('answers', [])
            
            assessment = self.assessment_service.get_by_id(assessment_id)
            if not assessment or assessment.user != request.user:
                return Response(
                    {'error': 'Assessment not found or access denied'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            checkin_date = timezone.now()
            created_answers = []
            
            for index, answer_data in enumerate(answers_data):
                # Get question by ID
                question_id = answer_data.get('question_id')
                if not question_id:
                    return Response(
                        {'error': 'question_id is required for each answer'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                question = self.question_service.get_by_id(question_id)
                if not question:
                    return Response(
                        {'error': f'Question with id {question_id} not found'},
                        status=status.HTTP_404_NOT_FOUND
                    )
                
                if question.category != 'checkin':
                    return Response(
                        {'error': f'Question {question_id} is not a check-in question'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                answer_text = answer_data.get('answer', '')
                selected_option_id = answer_data.get('selected_option')
                selected_option = None
                
                if selected_option_id:
                    selected_option = self.question_option_service.get_by_id(selected_option_id)
                    if not selected_option:
                        return Response(
                            {'error': f'Selected option with id {selected_option_id} not found'},
                            status=status.HTTP_404_NOT_FOUND
                        )

                    try:
                        validation_data = {
                            'question': question,
                            'selected_option': selected_option
                        }
                        self.question_option_service.validate(validation_data)
                    except ValueError as e:
                        return Response(
                            {'error': str(e)},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                
                if not answer_text and not selected_option:
                    return Response(
                        {'error': f'Either answer text or selected_option is required for question {question_id}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                try:
                    checkin_answer = self.assessment_answer_service.create(
                        assessment=assessment,
                        question=question,
                        answer=answer_text if answer_text else None,
                        selected_option=selected_option,
                        index=index,
                        is_checkin=True,
                        checkin_date=checkin_date
                    )
                    created_answers.append(checkin_answer)
                except Exception as e:
                    return Response(
                        {'error': f'Failed to create answer for question {question_id}: {str(e)}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            from apps.assessments.serializers.assessment_serializer import AssessmentSerializer
            assessment.refresh_from_db()
            serializer = AssessmentSerializer(assessment)
            return Response({
                'message': f'Successfully created {len(created_answers)} check-in answers',
                'assessment': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )