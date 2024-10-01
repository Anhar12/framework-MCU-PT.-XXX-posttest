from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Users, Regis, Result

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'role'),
        }),
    )
    list_display = ('email', 'username', 'role','is_staff', 'is_superuser')
    search_fields = ('email', 'username')
    ordering = ('email',)

admin.site.register(Users, UserAdmin)

@admin.register(Regis)
class RegisAdmin(admin.ModelAdmin):
    list_display = ('id_user', 'no_antrean', 'date', 'is_done')
    search_fields = ('id_user__email',)
    list_filter = ('is_done', 'date')
    
@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('id_mcu_regis', 'id_doctor', 'result', 'no_document', 'date')
    search_fields = ('id_mcu_regis__id_user__email', 'id_doctor__email', 'no_document')
    list_filter = ('result', 'date')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "id_mcu_regis":
            if 'add' in request.path:
                kwargs["queryset"] = Regis.objects.filter(is_done=False)
            else:
                kwargs["queryset"] = Regis.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_fields(self, request, obj=None):
        if 'add' in request.path:
            return ('id_mcu_regis', 'id_doctor', 'result', 'notes')
        return ('id_mcu_regis', 'id_doctor', 'result', 'no_document', 'date', 'notes')

    def get_readonly_fields(self, request, obj=None):
        if 'add' in request.path:
            return ()
        return ('no_document', 'date')