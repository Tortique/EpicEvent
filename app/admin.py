from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from app.models import User, Client

admin.site.unregister(Group)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (
            "Personal Info",
            {
                "fields": (
                    "username",
                    "password",
                    "first_name",
                    "last_name",
                    "email",
                    "phone",
                )
            },
        ),
        ("Permissions", {"fields": ("team",)}),
        ("Important Dates", {"fields": ("date_joined", "last_login")}),
    )
    readonly_fields = ("date_joined", "last_login")
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "phone",
        "team",
    )
    list_filter = ("team", "is_active")


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Client/Prospect Info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "company_name",
                    "email",
                    "phone",
                    "mobile",
                )
            },
        ),
        ("Sales", {"fields": ("status", "sales_contact")}),
        ("Info", {"fields": ("date_created", "date_updated")}),
    )
    readonly_fields = ("date_created", "date_updated")
    list_display = (
        "full_name",
        "company_name",
        "email",
        "phone",
        "mobile",
        "status",
        "sales_contact",
    )
    list_filter = ("status", "sales_contact")
    search_fields = ("first_name", "last_name", "company_name", "sales_contact")

    @staticmethod
    def full_name(obj):
        return f"{obj.last_name}, {obj.first_name}"
