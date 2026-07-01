from django.urls import path

from core import views
from core import views_directions
from core import views_payments
from core import views_reports
from core import views_schedule
from core import views_students
from core import views_teachers

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('subscriptions/', views.subscriptions_grid, name='subscriptions'),

    path('students/', views_students.student_list, name='student_list'),
    path('students/new/', views_students.student_create, name='student_create'),
    path('students/<uuid:pk>/', views_students.student_detail, name='student_detail'),
    path('students/<uuid:pk>/assign-direction/', views_students.student_assign_direction, name='student_assign_direction'),
    path('api/estimate-subscription/', views_students.estimate_subscription_api, name='estimate_subscription'),

    path('directions/', views_directions.direction_list, name='direction_list'),
    path('directions/new/', views_directions.direction_create, name='direction_create'),
    path('directions/<uuid:pk>/', views_directions.direction_detail, name='direction_detail'),
    path('directions/<uuid:pk>/delete/', views_directions.direction_delete, name='direction_delete'),

    path('teachers/', views_teachers.teacher_list, name='teacher_list'),
    path('teachers/new/', views_teachers.teacher_create, name='teacher_create'),
    path('teachers/<uuid:pk>/', views_teachers.teacher_detail, name='teacher_detail'),
    path('teachers/<uuid:pk>/assign-direction/', views_teachers.teacher_assign_direction, name='teacher_assign_direction'),
    path('teachers/<uuid:pk>/remove-direction/', views_teachers.teacher_remove_direction, name='teacher_remove_direction'),
    path('teachers/<uuid:pk>/delete/', views_teachers.teacher_delete, name='teacher_delete'),

    path('schedule/', views_schedule.schedule_page, name='schedule'),
    path('schedule/attendance/', views_schedule.schedule_save_attendance, name='schedule_save_attendance'),
    path('schedule/slot/save/', views_schedule.schedule_slot_save, name='schedule_slot_save'),
    path('schedule/slot/<uuid:pk>/duplicate/', views_schedule.schedule_slot_duplicate, name='schedule_slot_duplicate'),
    path('schedule/slot/<uuid:pk>/delete/', views_schedule.schedule_slot_delete, name='schedule_slot_delete'),
    path('schedule/reorder/', views_schedule.schedule_reorder, name='schedule_reorder'),
    path('schedule/direction-students/', views_schedule.schedule_direction_students, name='schedule_direction_students'),
    path('schedule/single/', views_schedule.schedule_add_single, name='schedule_add_single'),
    path('schedule/exception/', views_schedule.schedule_add_exception, name='schedule_add_exception'),

    path('reports/', views_reports.reports_dashboard, name='reports_dashboard'),
    path('reports/payments/', views_payments.payments_report, name='payments_report'),
    path('reports/payments/export/', views_payments.payments_export, name='payments_export'),
    path('reports/salary/', views_reports.salary_report, name='salary_report'),
    path('reports/profit/', views_reports.profit_report, name='profit_report'),
]
