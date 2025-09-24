from django.contrib import admin
from .models import (
    BagList, BagListSection, BagListItem, BagListItemProductSnapshot,
    Tag, BagListTag, FavoriteBagList, FavoriteProduct,
    Facet, FacetOption, BagListFacetValue,
    SectionFieldDef, BagListItemFieldValue
)

# -----------------------------------
# BagList y Secciones
# -----------------------------------
class BagListSectionInline(admin.TabularInline):
    model = BagListSection
    extra = 0
    fields = ("title", "position", "collapsed_by_default")
    ordering = ("position",)

class BagListItemInline(admin.TabularInline):
    model = BagListItem
    extra = 0
    fields = ("custom_title", "section", "position", "pin")
    ordering = ("section", "position")

@admin.register(BagList)
class BagListAdmin(admin.ModelAdmin):
    list_display = ("id","title", "owner", "visibility","slug", "published_at", "is_deleted")
    list_filter = ("visibility", "published_at", "is_deleted")
    search_fields = ("title", "owner__handle")
    inlines = [BagListSectionInline, BagListItemInline]

# -----------------------------------
# BagListSection
# -----------------------------------
@admin.register(BagListSection)
class BagListSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "baglist", "position", "collapsed_by_default")
    list_filter = ("baglist",)
    search_fields = ("title", "baglist__title")

# -----------------------------------
# BagListItem y snapshot
# -----------------------------------
@admin.register(BagListItem)
class BagListItemAdmin(admin.ModelAdmin):
    list_display = ("custom_title", "baglist", "section", "position", "pin")
    list_filter = ("baglist", "section", "pin")
    search_fields = ("custom_title", "baglist__title", "section__title")

@admin.register(BagListItemProductSnapshot)
class BagListItemProductSnapshotAdmin(admin.ModelAdmin):
    list_display = ("snap_title", "item", "snap_price_amount", "snap_price_currency")
    list_filter = ("snap_price_currency",)
    search_fields = ("snap_title", "item__custom_title", "item__baglist__title")

# -----------------------------------
# Tags y favoritos
# -----------------------------------
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "slug")
    search_fields = ("name", "owner__handle")

@admin.register(BagListTag)
class BagListTagAdmin(admin.ModelAdmin):
    list_display = ("baglist", "tag")
    list_filter = ("baglist", "tag")

@admin.register(FavoriteBagList)
class FavoriteBagListAdmin(admin.ModelAdmin):
    list_display = ("profile", "baglist")
    list_filter = ("baglist",)

@admin.register(FavoriteProduct)
class FavoriteProductAdmin(admin.ModelAdmin):
    list_display = ("profile", "item")
    list_filter = ("item",)

# -----------------------------------
# Facetas
# -----------------------------------
class FacetOptionInline(admin.TabularInline):
    model = FacetOption
    extra = 0
    fields = ("code", "label", "extra")

@admin.register(Facet)
class FacetAdmin(admin.ModelAdmin):
    list_display = ("key", "label")
    inlines = [FacetOptionInline]

@admin.register(FacetOption)
class FacetOptionAdmin(admin.ModelAdmin):
    list_display = ("facet", "code", "label")
    list_filter = ("facet",)
    search_fields = ("code", "label")

@admin.register(BagListFacetValue)
class BagListFacetValueAdmin(admin.ModelAdmin):
    list_display = ("baglist", "facet", "option", "numeric_value", "numeric_unit")
    list_filter = ("facet", "numeric_unit")
    search_fields = ("baglist__title", "option__label")

# -----------------------------------
# Campos personalizados de sección
# -----------------------------------
@admin.register(SectionFieldDef)
class SectionFieldDefAdmin(admin.ModelAdmin):
    list_display = ("section", "name", "key", "type", "unit", "is_primary", "position")
    list_filter = ("section", "type")
    search_fields = ("name", "key")

@admin.register(BagListItemFieldValue)
class BagListItemFieldValueAdmin(admin.ModelAdmin):
    list_display = ("item", "field", "value_text", "value_number", "value_bool", "value_enum")
    list_filter = ("field__type",)
    search_fields = ("item__custom_title", "field__name")
