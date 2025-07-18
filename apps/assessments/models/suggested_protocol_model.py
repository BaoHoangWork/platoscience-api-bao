from django.db import models
from .assessment_model import Assessment
from .protocol_model import Protocol

class SuggestedProtocol(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='suggested_protocols')
    first_protocol = models.ForeignKey(Protocol, on_delete=models.CASCADE, related_name='first_suggested_protocols', null=True, blank=True)
    second_protocol = models.ForeignKey(Protocol, on_delete=models.CASCADE, related_name='second_suggested_protocols', null=True, blank=True)
    third_protocol = models.ForeignKey(Protocol, on_delete=models.CASCADE, related_name='third_suggested_protocols', null=True, blank=True)

    class Meta:
        db_table = 'assessments_suggested_protocol'
