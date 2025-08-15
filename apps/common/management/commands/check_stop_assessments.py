from django.core.management.base import BaseCommand
from apps.assessments.services.assessment_service import AssessmentService

class Command(BaseCommand):
    help = 'Check and stop assessments out of period'

    def handle(self, *args, **options):
        try:
            service = AssessmentService()
            updated_count = service.end_assessment_period()
            self.stdout.write(self.style.SUCCESS(f"Stopped {updated_count} assessments."))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error: {str(e)}"))