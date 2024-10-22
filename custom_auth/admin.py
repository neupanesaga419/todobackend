from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ["username", "email", "is_staff"]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("profile_pic",)}),)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "profile_pic"]
    search_fields = ["user__username"]
    list_filter = ["user__is_staff"]
