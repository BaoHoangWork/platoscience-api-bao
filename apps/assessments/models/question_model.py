from django.db import models

class Question(models.Model):
    QUESTION_TYPES = [
        ('text', 'Text Input'),
        ('radio', 'Radio Button'),
        ('select', 'Dropdown Select'),
    ]
    
    QUESTION_CATEGORIES = [
        ('phq9', 'PHQ'),
        ('bdi', 'BDI'),
        ('normal', 'Normal'),
<<<<<<< HEAD
        ('analytic', 'Analytic'),
=======
>>>>>>> 3641a70 (update question model and swagger)
    ]
    
    name = models.CharField(max_length=255, unique=True)
    content = models.TextField()
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=50, choices=QUESTION_CATEGORIES, default='normal')
    type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='text')
