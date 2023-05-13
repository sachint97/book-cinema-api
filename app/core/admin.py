from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BasUserAdmin
from django.contrib.admin import ModelAdmin
from .models import *

# Register your models here.
class CityAdmin(ModelAdmin):
    list_display=["name","slug"]

class ShowsAdmin(ModelAdmin):
    list_display=["movie","start_date","end_date","start_time","end_time","slug"]

class ScreenShowMapperAdmin(ModelAdmin):
    list_display = ["show","screen","slug"]

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
admin.site.register(City,CityAdmin)
admin.site.register(Movie)
admin.site.register(Media)
admin.site.register(Theater)
admin.site.register(Screen)
admin.site.register(Show, ShowsAdmin)
admin.site.register(ScreenShowMapper, ScreenShowMapperAdmin)
admin.site.register(SeatingClass)
admin.site.register(Fare)
admin.site.register(Seat)
admin.site.register(Booking)
admin.site.register(BookingSeat)
admin.site.register(Payment)

