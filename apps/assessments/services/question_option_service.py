from apps.assessments.repositories.question_option_repository import QuestionOptionRepository
from apps.common.base_service import BaseService

class QuestionOptionService(BaseService):
    def __init__(self):
        super().__init__(QuestionOptionRepository())
    
    # Validate option-question pair 
    def validate(self, data):
        question = data.get("question")
        selected_option = data.get("selected_option")
        if not selected_option:
            return
        valid_option_question = self.repository.filter(question_id=question.id, id=selected_option.id)
        if not valid_option_question:
            raise ValueError(
                f"Selected option (id={selected_option.id}) does not belong to question (id={question.id})"
            )

    def sum_of_values(self, questions):
        sum = 0
        for question in questions:
            question_id = question["question"].id
            option_id = question["selected_option"]
            option = self.repository.filter(question_id=question_id, id=option_id).first()
            if option:
                sum += int(option.value)
        return sum