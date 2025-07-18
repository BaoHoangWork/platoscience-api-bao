from django.db import models

class Question(models.Model):
    name = models.CharField(max_length=255, unique=True)
    content = models.TextField()
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
