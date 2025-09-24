# common/models.py
from django.db import models

class TimeStampedModel(models.Model):
    """
    Modelo abstracto base que añade campos created_at y updated_at a cualquier modelo hijo.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
