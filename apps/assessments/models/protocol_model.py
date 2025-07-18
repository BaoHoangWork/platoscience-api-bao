from django.db import models

class Protocol(models.Model):
    intensity = models.CharField(max_length=255, blank=True, null=True)
    duration = models.CharField(max_length=255, blank=True, null=True)
    node_placement = models.CharField(max_length=255, blank=True, null=True)
    node_type = models.CharField(max_length=255, blank=True, null=True)
    node_size = models.CharField(max_length=255, blank=True, null=True)
