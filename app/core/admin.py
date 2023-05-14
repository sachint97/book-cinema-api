from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BasUserAdmin
from django.contrib.admin import ModelAdmin
from .models import *

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

class CityAdmin(ModelAdmin):
    list_display=["name","slug"]

class MovieAdmin(ModelAdmin):
    list_display= ["title","slug","description","duration","release_date",
                  "language","certificate"]

class TheaterAdmin(ModelAdmin):
    list_display = ["name","slug","address","city"]

class ScreenAdmin(ModelAdmin):
    list_display = ["name", "slug", "theater"]

class ShowsAdmin(ModelAdmin):
    list_display=["movie","start_date","end_date","start_time","end_time","slug"]

class ScreenShowMapperAdmin(ModelAdmin):
    list_display = ["show","screen","slug"]

class FareAdmin(ModelAdmin):
    list_display = ["screen_show","seating_class","price"]

class SeatAdmin(ModelAdmin):
    list_display = ["screen","fare","row","column","is_available"]

class BookingAdmin(ModelAdmin):
    list_display = ["user","booking_date","slug"]

class BookingSeatAdmin(ModelAdmin):
    list_display = ["seat","booking_status","booking","slug"]

class PaymentAdmin(ModelAdmin):
    list_display = ["amount","timestamp",
    "payment_method","booking","coupon","payment_status","slug"]




admin.site.register(User, UserAdmin)
admin.site.register(City,CityAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Media)
admin.site.register(Theater, TheaterAdmin)
admin.site.register(Screen, ScreenAdmin)
admin.site.register(Show, ShowsAdmin)
admin.site.register(ScreenShowMapper, ScreenShowMapperAdmin)
admin.site.register(SeatingClass)
admin.site.register(Fare, FareAdmin)
admin.site.register(Seat, SeatAdmin)
admin.site.register(Booking,BookingAdmin)
admin.site.register(BookingSeat, BookingSeatAdmin)
admin.site.register(Payment, PaymentAdmin)

