from apps.assessments.repositories.assessment_checkin_answer_repository import AssessmentCheckinAnswerRepository
from apps.common.base_service import BaseService

class AssessmentCheckinAnswerService(BaseService):
    def __init__(self):
        super().__init__(AssessmentCheckinAnswerRepository())

    def can_checkin_today(self, assessment):
        return not self.repository.has_checkin_today(assessment)

    def get_checkin_history(self, assessment):
        history = self.repository.get_checkin_answers_grouped_by_date(assessment)
        result = []
        for day, answers in sorted(history.items(), reverse=True):
            result.append({
                'date': day,
                'answers': answers
            })
        return result