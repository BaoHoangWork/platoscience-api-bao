from rest_framework.test import APITestCase, APIClient
from apps.users.models import User
from apps.assessments.models import Assessment, Protocol

class AssessmentTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email="user@gmail.com",
            password="password123"
        )

        self.protocol = Protocol.objects.create(
            intensity="High",
            duration="30 mins",
            node_placement="Head",
            node_type="Type A",
            node_size="Large"
        )

        self.assessment1 = Assessment.objects.create(
            user=self.user,
            phq_score=15,
            bdi_score=30,
            plato_score=3.5,
            protocol=self.protocol,
            severity=2
        )

        self.assessment2 = Assessment.objects.create(
            user=self.user,
            phq_score=10,
            bdi_score=20,
            plato_score=2.0,
            protocol=self.protocol,
            severity=1
        )
        
        self.answer1 = {
            "assessment": self.assessment1.id,
            "question": "What is your mood today?",
            "answer": "I feel anxious and stressed."
        }
        
        self.answer2 = {
            "assessment": self.assessment2.id,
            "question": "How well did you sleep last night?",
            "answer": "I slept poorly and woke up several times."
        }

        self.client.force_authenticate(user=self.user)
        
        self.get_all_by_user_url = '/api/assessments/'
    
    def test_get_all_by_user(self):
        response = self.client.get(self.get_all_by_user_url)
        return response
