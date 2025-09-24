# lists/models.py
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import Profile
from common.models import TimeStampedModel
from catalog.models import ExternalProduct

class ListVisibility(models.TextChoices):
    """
    Opciones de visibilidad para una BagList.
    """
    PRIVATE = "private", _("Private")          # Solo el owner y usuarios con acceso explícito
    UNLISTED = "unlisted", _("Unlisted")      # Accesible por URL con token, no indexa en buscadores
    REGISTERED = "registered", _("Registered users")  # Visible solo para usuarios logueados
    PUBLIC = "public", _("Public")            # Visible para cualquier persona y indexable

class BagList(TimeStampedModel):
    """
    Modelo principal de BagList.
    Representa una lista de productos de un usuario, p.ej. “Mochila de Japón”.
    """
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )  # Identificador único global

    owner = models.ForeignKey(
        Profile, 
        on_delete=models.CASCADE, 
        related_name="baglists"
    )  # Perfil del usuario que crea la lista

    title = models.CharField(max_length=200)
    """Nombre visible de la BagList, p.ej. 'Mochila de Japón'"""

    description = models.TextField(blank=True)
    """Descripción opcional de la BagList"""

    slug = models.SlugField(max_length=100)
    """Slug único por owner para URL bonita, p.ej. /@handle/baglist/mi-setup"""

    visibility = models.CharField(
        max_length=12,
        choices=ListVisibility.choices,
        default=ListVisibility.PRIVATE,
        db_index=True,
    )
    """Controla quién puede ver la BagList"""

    cover_image_url = models.URLField(blank=True)
    """Imagen de portada de la BagList"""

    allow_forks = models.BooleanField(default=True)
    """Si otros usuarios pueden clonar/copiar esta BagList"""

    share_token = models.CharField(
        max_length=64, 
        blank=True, 
        null=True, 
        unique=True
    )
    """Token para listas 'unlisted', permite acceso por URL privada"""

    published_at = models.DateTimeField(
        null=True, 
        blank=True, 
        db_index=True
    )
    """Fecha de publicación; útil para ordenar cronológicamente y SEO"""

    is_deleted = models.BooleanField(default=False)
    """Soft-delete: marca si la BagList ha sido eliminada"""

    deleted_at = models.DateTimeField(null=True, blank=True)
    """Fecha de eliminación (soft-delete)"""

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["owner", "slug"], name="uniq_baglist_owner_slug"),
        ]
        """Evita que un mismo usuario tenga dos BagLists con el mismo slug"""

    def __str__(self):
        return f"{self.title} (@{self.owner.handle})"
class BagListSection(TimeStampedModel):
    """
    Sección dentro de una BagList.
    Ejemplos: “Tecnología”, “Ropa”, “Higiene”.
    Permite organizar los BagListItems dentro de la lista principal.
    """
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )  # Identificador único global

    baglist = models.ForeignKey(
        BagList, 
        on_delete=models.CASCADE, 
        related_name="sections"
    )
    """La BagList a la que pertenece esta sección"""

    title = models.CharField(max_length=120)
    """Nombre de la sección, p.ej. 'Tecnología'"""

    description = models.TextField(blank=True)
    """Descripción opcional de la sección"""

    position = models.PositiveIntegerField(db_index=True)
    """Orden de la sección dentro de la BagList; valores bajos = arriba"""

    collapsed_by_default = models.BooleanField(default=False)
    """Indica si la sección aparece plegada por defecto en la UI"""

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["baglist", "position"], name="uniq_section_baglist_pos"),
        ]
        """Evita que dos secciones tengan la misma posición dentro de la misma BagList"""

    def __str__(self):
        return f"{self.title} ({self.baglist.title})"
    

class BagListItem(TimeStampedModel):
    """
    Producto o item dentro de una BagListSection.
    Cada BagListItem pertenece a una sección y a una BagList.
    """
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )  # Identificador único global

    baglist = models.ForeignKey(
        BagList, 
        on_delete=models.CASCADE, 
        related_name="items"
    )
    """La BagList a la que pertenece este item"""

    section = models.ForeignKey(
        BagListSection, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="items"
    )
    """Sección dentro de la BagList; puede ser null si aún no se asigna"""

    position = models.PositiveIntegerField(db_index=True)
    """Posición dentro de la sección; valores bajos = arriba"""

    note = models.TextField(blank=True)
    """Notas o comentarios del usuario sobre este item"""

    pin = models.BooleanField(default=False)
    """Si el item está fijado/destacado dentro de la sección"""

    custom_title = models.CharField(max_length=200, blank=True)
    """Título personalizado opcional para mostrar en la UI"""

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["baglist", "position"], name="uniq_item_baglist_pos"),
        ]
        """Evita que dos items tengan la misma posición dentro de la misma BagList"""

    def __str__(self):
        return f"{self.custom_title or 'Item'} ({self.baglist.title})"



class BagListItemProductSnapshot(TimeStampedModel):
    """
    Snapshot de un producto externo vinculado a un BagListItem.
    Permite mantener un registro de los datos del producto en el momento en que se añadió,
    independientemente de cambios futuros en ExternalProduct.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    item = models.OneToOneField(
        BagListItem,
        on_delete=models.CASCADE,
        related_name="snapshot"
    )
    """Referencia al BagListItem correspondiente"""

    external_product = models.ForeignKey(
        ExternalProduct,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    """Producto externo “canónico” vinculado a este item"""

    snap_title = models.CharField(max_length=255)
    """Título del producto en el momento del snapshot"""

    snap_image_url = models.URLField(blank=True)
    """Imagen del producto en el momento del snapshot"""

    snap_price_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    """Precio del producto en el momento del snapshot"""

    snap_price_currency = models.CharField(max_length=3, blank=True)
    """Moneda del precio"""

    affiliate_url = models.TextField(blank=True)
    """URL de afiliado (si aplica)"""

    canonical_url = models.TextField(blank=True)
    """URL canónica del producto"""

    coupon_code = models.CharField(max_length=80, blank=True)
    """Código de cupón asociado, si existe"""

    coupon_expires_at = models.DateTimeField(null=True, blank=True)
    """Fecha de expiración del cupón"""

    video_url = models.URLField(blank=True)
    """URL de video asociado al producto"""

    extra_links = models.JSONField(default=list, blank=True)
    """Lista de enlaces adicionales (reviews, webs, etc.)"""

    def __str__(self):
        return f"{self.snap_title} ({self.item.baglist.title})"


class Tag(TimeStampedModel):
    """
    Etiqueta que un usuario puede crear para organizar sus BagLists.
    Cada tag pertenece a un Profile.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    owner = models.ForeignKey(
        "accounts.Profile",
        on_delete=models.CASCADE,
        related_name="tags"
    )
    """Usuario propietario del tag"""

    name = models.CharField(max_length=60)
    """Nombre visible de la etiqueta"""

    slug = models.SlugField(max_length=80)
    """Slug técnico único por usuario"""

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["owner", "slug"], name="uniq_tag_owner_slug"),
        ]
        """Evita que un usuario tenga dos tags con el mismo slug"""

    def __str__(self):
        return f"{self.name} (@{self.owner.handle})"


class BagListTag(models.Model):
    """
    Relación muchos a muchos entre BagList y Tag.
    Permite asociar múltiples tags a una BagList y reutilizar tags.
    """
    baglist = models.ForeignKey(BagList, on_delete=models.CASCADE)
    """BagList a la que se aplica el tag"""

    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    """Tag aplicado a la BagList"""

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["baglist", "tag"], name="uniq_baglist_tag"),
        ]
        """Evita que un mismo tag se aplique varias veces a la misma BagList"""

    def __str__(self):
        return f"{self.baglist.title} -> {self.tag.name}"
class FavoriteBagList(TimeStampedModel):
    """
    Permite a un Profile marcar una BagList como favorita.
    """
    profile = models.ForeignKey(
        "accounts.Profile",
        on_delete=models.CASCADE
    )
    """Usuario que marca la BagList como favorita"""

    baglist = models.ForeignKey(
        BagList,
        on_delete=models.CASCADE
    )
    """BagList marcada como favorita"""

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["profile", "baglist"], name="uniq_fav_baglist"),
        ]
        """Evita duplicados: un usuario solo puede marcar una vez la misma BagList"""

    def __str__(self):
        return f"{self.profile.handle} ❤️ {self.baglist.title}"


class FavoriteProduct(TimeStampedModel):
    """
    Permite a un Profile marcar un BagListItem como favorito.
    """
    profile = models.ForeignKey(
        "accounts.Profile",
        on_delete=models.CASCADE
    )
    """Usuario que marca el producto como favorito"""

    item = models.ForeignKey(
        BagListItem,
        on_delete=models.CASCADE
    )
    """BagListItem marcado como favorito"""

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["profile", "item"], name="uniq_fav_item"),
        ]
        """Evita duplicados: un usuario solo puede marcar una vez el mismo producto"""

    def __str__(self):
        return f"{self.profile.handle} ❤️ {self.item.custom_title or 'Item'}"

# lists/models.py (continuación)

class FacetKey(models.TextChoices):
    """
    Claves de facetas predefinidas para filtrar BagLists.
    """
    COUNTRY = "country"
    SEASON = "season"
    DURATION = "duration"
    USE = "use"


class Facet(TimeStampedModel):
    """
    Define un tipo de faceta que se puede asignar a BagLists.
    Ejemplo: país, temporada, uso, duración.
    """
    key = models.CharField(max_length=40, choices=FacetKey.choices, unique=True)
    """Clave de la faceta (estable)"""

    label = models.CharField(max_length=80)
    """Etiqueta visible en la UI"""

    def __str__(self):
        return self.label


class FacetOption(TimeStampedModel):
    """
    Opciones concretas de cada faceta.
    Ejemplo: facet=country → code=ES, label=España
             facet=season → code=summer, label=Verano
    """
    facet = models.ForeignKey(Facet, on_delete=models.CASCADE, related_name="options")
    code = models.SlugField(max_length=80)
    """Código técnico de la opción"""

    label = models.CharField(max_length=120)
    """Etiqueta visible"""

    extra = models.JSONField(default=dict, blank=True)
    """Metadatos extra (iconos, ISO, etc.)"""

    class Meta:
        unique_together = ("facet", "code")
        """Evita duplicados: no puede haber dos opciones iguales para la misma faceta"""

    def __str__(self):
        return f"{self.facet.key}: {self.label}"


class DurationUnit(models.TextChoices):
    """
    Unidades para duración, usadas en BagListFacetValue.
    """
    HOURS = "h"
    DAYS = "d"
    WEEKS = "w"


class BagListFacetValue(TimeStampedModel):
    """
    Valor de faceta asignado a una BagList.
    - Para country/season/use → se usa 'option'
    - Para duration → se usan numeric_value + numeric_unit
    """
    baglist = models.ForeignKey(BagList, on_delete=models.CASCADE, related_name="facet_values")
    facet = models.ForeignKey(Facet, on_delete=models.CASCADE)
    option = models.ForeignKey(FacetOption, null=True, blank=True, on_delete=models.SET_NULL)
    """Para facetas tipo country/season/use"""

    numeric_value = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    """Valor numérico para duración"""

    numeric_unit = models.CharField(max_length=2, choices=DurationUnit.choices, blank=True)
    """Unidad de duración"""

    class Meta:
        indexes = [models.Index(fields=["baglist", "facet"])]
        constraints = [
            models.UniqueConstraint(fields=["baglist", "facet", "option"], name="uniq_baglist_facet_option"),
        ]
        """Evita duplicar la misma opción de faceta para una BagList"""

    def __str__(self):
        if self.option:
            return f"{self.baglist.title} → {self.facet.key}: {self.option.label}"
        elif self.numeric_value:
            return f"{self.baglist.title} → {self.facet.key}: {self.numeric_value}{self.numeric_unit}"
        return f"{self.baglist.title} → {self.facet.key}"

# lists/models.py (continuación)

class FieldType(models.TextChoices):
    """
    Tipos de campos soportados en SectionFieldDef.
    Se usan para ordenar, filtrar y mostrar en la UI.
    """
    TEXT = "text"
    NUMBER = "number"
    BOOLEAN = "bool"
    DATE = "date"
    ENUM = "enum"
    URL = "url"


class SectionFieldDef(TimeStampedModel):
    """
    Define un “campo” o columna personalizada dentro de una BagListSection.
    Ejemplos:
      - Tecnología: battery_capacity (unit=mAh), weight (unit=g)
      - Cocina: capacity (unit=L), material (enum=[metal, plastic])
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    section = models.ForeignKey(
        BagListSection,
        on_delete=models.CASCADE,
        related_name="fields"
    )
    name = models.CharField(max_length=80)
    """Etiqueta visible (Peso, Capacidad, Material, etc.)"""

    key = models.SlugField(max_length=80)
    """Clave técnica estable (weight, capacity, material)"""

    type = models.CharField(max_length=10, choices=FieldType.choices)
    """Tipo de dato"""

    unit = models.CharField(max_length=20, blank=True)
    """Unidad sugerida (kg, g, cm, L…)"""

    enum_options = models.JSONField(default=list, blank=True)
    """Opciones permitidas si type=ENUM"""

    position = models.PositiveIntegerField(default=0, db_index=True)
    """Orden de la columna dentro de la sección"""

    is_primary = models.BooleanField(default=False)
    """Indica si es columna destacada en la UI"""

    class Meta:
        unique_together = ("section", "key")
        """No se pueden repetir keys dentro de la misma sección"""

    def __str__(self):
        return f"{self.section.title} → {self.name}"


class BagListItemFieldValue(TimeStampedModel):
    """
    Valor de un campo para un BagListItem concreto.
    Solo se debe rellenar la columna correspondiente al tipo de Field.
    """
    item = models.ForeignKey(
        BagListItem,
        on_delete=models.CASCADE,
        related_name="field_values"
    )
    field = models.ForeignKey(
        SectionFieldDef,
        on_delete=models.CASCADE,
        related_name="values"
    )

    # Valores según tipo de campo
    value_text = models.TextField(blank=True)
    value_number = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    value_bool = models.BooleanField(null=True, blank=True)
    value_date = models.DateField(null=True, blank=True)
    value_enum = models.CharField(max_length=80, blank=True)
    value_url = models.URLField(blank=True)

    class Meta:
        unique_together = ("item", "field")
        """Un item no puede tener dos valores para el mismo campo"""
        indexes = [
            models.Index(fields=["field", "value_number"]),
            models.Index(fields=["field", "value_text"]),
            models.Index(fields=["field", "value_enum"]),
        ]

    def __str__(self):
        return f"{self.item.custom_title or 'Item'} → {self.field.name}"
