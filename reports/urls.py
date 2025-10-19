from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('post/<int:post_id>/', views.report_post, name='report_post'),
    path('user/<str:username>/', views.report_user, name='report_user'),
    path('admin/', views.admin_reports, name='admin_reports'),
    path('admin/<int:report_id>/resolve/', views.resolve_report, name='resolve_report'),
]