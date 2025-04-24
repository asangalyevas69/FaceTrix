from rest_framework import serializers

from .models import Group, Student, Lesson, Attendance, Parent, Teacher

class GroupSerializers(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = "__all__"
        

class StudentSerializers(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = "__all__"
        read_only_fields = ['full_name, group']


class LessonSerializers(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = "__all__"


class AttendanceSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Attendance
        fields = "__all__"



class ParentSerializers(serializers.ModelSerializer):

    class Meta:
        model = Parent
        fields = "__all__"
        read_only_fields = ['name, student']


class TeacherSerializers(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = "__all__"
