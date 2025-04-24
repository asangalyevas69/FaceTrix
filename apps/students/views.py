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

"""Отчёт по студенту через ID"""
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

"""Отчёт по родителю через ID"""
class GetParentReportAPIView(APIView):
    def get(self, request, login_code):
        parent = Parent.objects.filter(login_code=login_code).first()#telegram_id na login_code

        if not parent:
            return Response({
                "student": "Родитель не найден",
                "total": 0,
                "present": 0,
                "absent": 0
            })

        student = parent.student
        total = Attendance.objects.filter(student=student).count()
        present = Attendance.objects.filter(student=student, attendance=True).count()
        absent = total - present

        return Response(data={
            "student": student.full_name,
            "total": total,
            "present": present,
            "absent": absent
        })

"""Отчёт по студенту через ID"""
class GetStudentReportAPIView(APIView):
    def get(self, request, login_code):
        student = Student.objects.filter(login_code=login_code).first()

        if not student:
            return Response({
                "student": "Студент не найден",
                "total": 0,
                "present": 0,
                "absent": 0
            })

        total = Attendance.objects.filter(student=student).count()
        present = Attendance.objects.filter(student=student, attendance=True).count()
        absent = total - present

        return Response({
            "student": student.full_name,
            "total": total,
            "present": present,
            "absent": absent
        })
