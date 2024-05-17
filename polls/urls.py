from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name='index'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('admin', views.admin, name='admin'),
    path('admin/admin_roaster',views.admin_roaster,name='admin_roaster'),
    path('admin/add_instructor', views.add_instructor, name='add_instructor'),
    path('admin/admin_salary',views.admin_salary,name='admin_salary'),
    path('admin/admin_performance',views.admin_performance,name='admin_performance'),
    path('instructor', views.instructor, name='instructor'),
    path('instructor/course_section', views.course_section,name='course_section'),
    path('instructor/student_enrolled_courses', views.student_enrolled_courses,name='student_enrolled_courses'),
    path('student', views.student, name='student'),
    path('query/courseSections', views.query_course_sections, name='query_course_sections'),
    path('courseSections_list', views.display_course_sections, name='courseSections_list'),

]