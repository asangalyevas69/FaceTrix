from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Group, Parent, Teacher, Student, Attendance, Lesson
from .serializers import GroupSerializers, StudentSerializers, TeacherSerializers, AttendanceSerializers, LessonSerializers, ParentSerializers



class GroupListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = GroupSerializers
    queryset = Group.objects.all()

class GroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GroupSerializers
    queryset = Group.objects.all()

class ParentListCreateView(generics.ListCreateAPIView):
    serializer_class = ParentSerializers
    queryset = Parent.objects.all()

class TeacherListCreateView(generics.ListCreateAPIView):
    serializer_class = TeacherSerializers
    queryset = Teacher.objects.all()

class StudentListCreateView(generics.ListCreateAPIView):
    serializer_class = StudentSerializers
    queryset = Student.objects.all()

class AttendanceCreateView(generics.ListCreateAPIView):
    serializer_class = AttendanceSerializers
    queryset = Attendance.objects.all()

class LessonCreateView(generics.ListCreateAPIView):
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()


class ParentReportAPIView(APIView):

    def get(self, request, student_id):
        total = Attendance.objects.filter(student_id=student_id).count()
        present = Attendance.objects.filter(student_id=student_id, attendance=True).count()
        absent = total - present

        return Response({
            "Присутствуют": present,
            "Отсутствуют": absent,
            "Всего": total,
        })