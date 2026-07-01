from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html

from accounts.models import StaffRole, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    extra = 0
    fields = ('role',)
    verbose_name = 'Доступ в CRM'
    verbose_name_plural = 'Доступ в CRM'

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        field = super().formfield_for_choice_field(db_field, request, **kwargs)
        if db_field.name == 'role':
            field.help_text = (
                'Директор — оплаты, отчёты, настройки (Django admin). '
                'Ресепшн — ученики, расписание, абонементы; без финансов.'
            )
        return field


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'crm_role', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'profile__role')

    @admin.display(description='Роль CRM')
    def crm_role(self, obj):
        if hasattr(obj, 'profile'):
            role = obj.profile.get_role_display()
            if obj.profile.role == StaffRole.DIRECTOR:
                return format_html('<strong>{}</strong>', role)
            return role
        return '—'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not hasattr(obj, 'profile'):
            role = StaffRole.DIRECTOR if obj.is_superuser else StaffRole.RECEPTION
            UserProfile.objects.create(user=obj, role=role)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
