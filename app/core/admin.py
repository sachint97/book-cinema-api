from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BasUserAdmin
from .models import User

# Register your models here.


class UserAdmin(BasUserAdmin):
    """Define the admin pages for users."""

    ordering = ["id"]
    list_display = ["email", "name", "phone","slug"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (("permissions"), {
            "fields": ("is_active", "is_staff", "is_superuser")
            }),
        (("Important dates", {"fields": ("last_login", "deleted_at")})),
    )
    readonly_fields = ["last_login", "created_at", "updated_at"]
    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "email",
                    "password1",
                    "password2",
                    "phone",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
    )


admin.site.register(User, UserAdmin)
