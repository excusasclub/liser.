# accounts/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile

User = get_user_model()

# Inline para mostrar el Profile dentro del User
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"

# Extendemos el UserAdmin original para añadir el inline
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

# Desregistramos el admin original de User
admin.site.unregister(User)
# Registramos nuestro UserAdmin con el inline de Profile
admin.site.register(User, UserAdmin)

# También registramos Profile de forma independiente si quieres verlo por sí solo
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "handle", "display_name", "is_creator")
    search_fields = ("handle", "display_name", "user__username", "user__email")
