# catalog/models.py
import uuid
from django.db import models
from common.models import TimeStampedModel

class ExternalProduct(TimeStampedModel):
    """
    Producto externo que puede vincularse a un BagListItem.
    Se puede ampliar más adelante con todos los campos reales.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    url = models.URLField(blank=True)

    def __str__(self):
        return self.name
