from django.contrib import admin
from .models.Users import Users

@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('username',)
    fields = ('email', 'username', 'role', 'is_staff', 'is_active', 'password')