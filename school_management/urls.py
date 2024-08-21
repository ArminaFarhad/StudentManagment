
from django.urls import path
from schools import views

urlpatterns = [
    path('student/grades/', views.student_grades, name='student_grades'),
    path('teacher/assign-grade/', views.assign_grade, name='assign_grade'),
    path('login-teacher/', views.loginTeacher, name='login'),
    path('login-student/', views.loginStudents, name='login'),
    path('get-subject-students/', views.GetSubjectStudents, name='subject-student'),
    path('assign-grade/', views.assign_grade, name='login'),
    path('get-subjects/', views.GetTeachersSubjects, name='subjects'),
]
