from django.contrib import admin
from .models import Student, Parent, Group, Teacher, Lesson


class ParentInline(admin.StackedInline):
    model = Parent
    max_num = 2
    readonly_fields = ['login_code']



@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    info = ('full_name', 'group')
    inlines = [ParentInline]
    group = ('group')
    readonly_fields = ['login_code']

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    info = ['group_name']


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['subject_name', 'teacher', 'group', 'time']
    list_filter = ['group', 'teacher']
    search_fields = ['subject_name']