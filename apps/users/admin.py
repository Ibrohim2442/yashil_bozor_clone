from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, UserProfile, Favorite


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Displayed fields in list view it's not fields!
    list_display = ("id", "phone", "is_staff", "is_active", "date_joined", "last_login")
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("phone",)
    ordering = ("-date_joined",)
    readonly_fields = ("date_joined", "last_login")

    # Remove username and email
    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("phone", "password1", "password2", "is_active", "is_staff", "is_superuser"),
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user_phone", "first_name", "last_name", "email", "gender", "created_at", "updated_at")
    list_filter = ("gender", "created_at", "updated_at")
    search_fields = ("first_name", "last_name", "user__phone", "email")
    readonly_fields = ("created_at", "updated_at")

    def user_phone(self, obj):
        return obj.user.phone
    user_phone.short_description = "Phone"

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__phone", "product__name")