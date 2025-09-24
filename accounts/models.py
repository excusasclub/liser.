# accounts/models.py
import uuid
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import TimeStampedModel  # Modelo base con created_at y updated_at

class Profile(TimeStampedModel):
    """
    Perfil público del usuario. 'handle' será el identificador público único.
    Guardamos enlaces sociales en 'links' para flexibilidad (JSON).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    handle = models.SlugField(unique=True, max_length=40)  # @handle único global
    display_name = models.CharField(max_length=120)         # Nombre para mostrar
    bio = models.TextField(blank=True)                      # Biografía corta
    avatar_url = models.URLField(blank=True)                # Foto de perfil
    links = models.JSONField(default=dict, blank=True)      # Enlaces sociales {instagram, youtube, web, ...}
    is_creator = models.BooleanField(default=False, db_index=True)  # Marca si es creador de contenido

    def __str__(self):
        return f"{self.display_name} (@{self.handle})"

