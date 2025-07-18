from django.db import models
from apps.users.models import User
from apps.assessments.models.protocol_model import Protocol
from django.core.validators import MinValueValidator, MaxValueValidator

SEVERITY_CHOICES = [
    (1, 'Mild'),
    (2, 'Moderate'),
    (3, 'Severe'),
    (4, 'Critical'),
]

class Assessment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assessments')
    phq_score = models.IntegerField(
        null=True, 
        blank=True, 
        validators=[MinValueValidator(0), MaxValueValidator(27)]
    )
    bdi_score = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(63)])
    plato_score = models.FloatField(null=True, blank=True)
    protocol = models.ForeignKey(
        Protocol, 
        on_delete=models.SET_NULL, 
        related_name='assessments', 
        null=True, 
        blank=True
    )
    severity = models.IntegerField(choices=SEVERITY_CHOICES, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
