from django.urls import path
from . import views


urlpatterns = [
    path('student/', views.StudentListCreateView.as_view()),
    path('group/', views.GroupListCreateAPIView.as_view()),
    path('group/<int:pk>/', views.GroupDetailView.as_view()),  
    path('teacher/', views.TeacherListCreateView.as_view()),
    path('lesson/', views.LessonCreateView.as_view()),
    path('attendance/', views.AttendanceCreateView.as_view()),
    path('parent/', views.ParentListCreateView.as_view()),
    path('api/report/<int:student_id>/', views.ParentReportAPIView.as_view()),
    path('api/parenttg/<str:login_code>/', views.GetParentReportAPIView.as_view()),
    path('api/studenttg/<str:login_code>/', views.GetStudentReportAPIView.as_view()),
    path('api/teachertg/<str:login_code>/', views.GetTeacherInfoAPIView.as_view()),
    path('api/teacher-groups/<str:login_code>/', views.TeacherGroupsAPIView.as_view()),
    path('api/group-attendance/<int:group_id>/', views.LastLessonAttendanceAPIView.as_view()),
]
