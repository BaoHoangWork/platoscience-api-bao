from django.core.management.base import BaseCommand
from apps.users.models import User
from apps.assessments.models import Assessment, Protocol

class Command(BaseCommand):
    help = 'Seed the database with user and assessment data'

    def handle(self, *args, **kwargs):
        user1 = User.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            is_staff=False,
            is_verified=True,
            password="password123"
        )
        user2 = User.objects.create(
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@example.com",
            is_staff=False,
            is_verified=True,
            password="password123"
        )

        protocol1 = Protocol.objects.create(
            intensity="High",
            duration="30 mins",
            node_placement="Head",
            node_type="Type A",
            node_size="Large"
        )
        protocol2 = Protocol.objects.create(
            intensity="Medium",
            duration="20 mins",
            node_placement="Chest",
            node_type="Type B",
            node_size="Medium"
        )

        # Create Assessments
        Assessment.objects.create(
            user=user1,
            phq_score=15,
            bdi_score=30,
            plato_score=3.5,
            protocol=protocol1,
            severity=2
        )
        Assessment.objects.create(
            user=user2,
            phq_score=10,
            bdi_score=20,
            plato_score=2.0,
            protocol=protocol2,
            severity=1
        )
        Assessment.objects.create(
            user=user1,
            phq_score=10,
            bdi_score=20,
            plato_score=2.0,
            protocol=protocol2,
            severity=1
        )

        self.stdout.write(self.style.SUCCESS('Successfully seeded user and assessment data'))
