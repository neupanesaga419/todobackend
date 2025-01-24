from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from custom_auth.models import CustomUser

# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ["username", "email", "is_staff", "is_active"]


admin.site.register(CustomUser, CustomUserAdmin)
