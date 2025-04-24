from django.urls import path

from . import views

urlpatterns = [
    path('student/', view=views.StudentListCreateView.as_view()),
    path('group/', view=views.GroupListCreateAPIView.as_view()),
    path('group/<int:pk>', view=views.GroupListCreateAPIView.as_view()),
    path('teacher/', view=views.TeacherListCreateView.as_view()),
    path('lesson/', view=views.LessonCreateView.as_view()),
    path('attendance/', view=views.AttendanceCreateView.as_view()),
    path('parent/', view=views.ParentListCreateView.as_view())
]
