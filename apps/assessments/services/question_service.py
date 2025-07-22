from collections import defaultdict
from apps.assessments.repositories.question_repository import QuestionRepository
from apps.common.base_service import BaseService

class QuestionService(BaseService):
    def __init__(self):
        super().__init__(QuestionRepository())
    
    def group_questions_by_category(self, requested_category, answers_data):
        try:
            questions = []
            for answer in  answers_data:
                if not answer.get("selected_option"):
                    continue 
                matching_question = self.filter(category=requested_category, id=answer.get("question").id)
                if matching_question:
                    if requested_category=="text" or requested_category=="analytic":
                        questions.append({
                            "question": matching_question[0],
                            "answer": answer.get("answer")
                        })
                    else:
                        questions.append({
                            "question": matching_question[0],
                            "selected_option": answer.get("selected_option").id
                        })
            return questions
        except Exception as e:
            raise Exception(f"Error group questions: {str(e)}")
