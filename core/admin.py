from django.contrib import admin

from core.models import (
    AttendanceRecord,
    AuditLog,
    CenterSettings,
    Classroom,
    Direction,
    KanbanTask,
    MaterialPurchase,
    NewsItem,
    Parent,
    Payment,
    ScheduleException,
    ScheduleSlot,
    SingleLesson,
    Student,
    SubDirection,
    Subscription,
    Teacher,
)


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'lesson_type', 'price_per_lesson', 'single_lesson_cost', 'subscription_cost', 'min_age', 'max_age')
    search_fields = ('name',)


@admin.register(SubDirection)
class SubDirectionAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'parent')
    list_filter = ('parent',)


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email')
    search_fields = ('name', 'phone')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'date_of_birth', 'registration_date')
    search_fields = ('name',)
    filter_horizontal = ('directions',)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'hire_date')
    search_fields = ('name',)
    filter_horizontal = ('directions',)


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity')


@admin.register(ScheduleSlot)
class ScheduleSlotAdmin(admin.ModelAdmin):
    list_display = ('direction', 'student', 'get_day_of_week_display', 'start_time', 'end_time', 'teacher', 'is_archived')
    list_filter = ('day_of_week', 'direction', 'is_archived')


@admin.register(ScheduleException)
class ScheduleExceptionAdmin(admin.ModelAdmin):
    list_display = ('lesson_date', 'schedule_slot', 'exception_type', 'substitute_teacher')
    list_filter = ('exception_type',)


@admin.register(SingleLesson)
class SingleLessonAdmin(admin.ModelAdmin):
    list_display = ('student', 'direction', 'lesson_date', 'lesson_type', 'teacher')
    list_filter = ('lesson_type', 'direction')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'direction', 'payment_date', 'amount', 'payment_type')
    list_filter = ('payment_type', 'direction', 'payment_date')
    date_hierarchy = 'payment_date'


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'student', 'direction', 'start_date', 'end_date',
        'total_lessons', 'carried_lessons', 'amount', 'status',
    )
    list_filter = ('status', 'direction')
    date_hierarchy = 'start_date'


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson_date', 'direction', 'present', 'paid')
    list_filter = ('present', 'paid', 'direction', 'lesson_date')
    date_hierarchy = 'lesson_date'


@admin.register(MaterialPurchase)
class MaterialPurchaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'direction', 'total_cost', 'purchase_date')
    date_hierarchy = 'purchase_date'


@admin.register(KanbanTask)
class KanbanTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'assignee')
    list_filter = ('status',)


@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ('published_date', 'author')
    date_hierarchy = 'published_date'


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'action')
    list_filter = ('action',)
    readonly_fields = ('timestamp', 'user', 'action', 'details')


@admin.register(CenterSettings)
class CenterSettingsAdmin(admin.ModelAdmin):
    list_display = ('trial_cost', 'single_cost_multiplier')

    def has_add_permission(self, request):
        return not CenterSettings.objects.exists()
