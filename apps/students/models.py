from django.db import models

import random

from datetime import timedelta

class Group(models.Model):
    """
    Model for group
    """
    group_name = models.CharField(max_length=50)
    teacher = models.ForeignKey("Teacher", on_delete=models.CASCADE, related_name="groups", null=True)


    def __str__(self):
        return self.group_name


class Student(models.Model):
    """
    Models for student
    """
    full_name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='faces/')
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    login_code = models.CharField(max_length=6, unique=True) 

    def save(self, *args, **kwargs):
        if not self.login_code:
            self.login_code = str(random.randint(100000, 999999))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name



class Teacher(models.Model):
    """
    models for Teacher
    """
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=15, default="0700000000")
    login_code = models.CharField(max_length=6, unique=True, blank=True)

    def save(self, *args, **kwargs):
            if not self.login_code:
                while True:
                    code = str(random.randint(100000, 999999))
                    if not Teacher.objects.filter(login_code=code).exists():
                        self.login_code = code
                        break
            super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    
class Lesson(models.Model):
    """
    Models for Lesson
    """
    subject_name = models.CharField(max_length=100)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True, editable=False)
    
    
    def __str__(self):
        return f"{self.subject_name}-{self.time}"
    

    def save(self, *args, **kwargs):
        if not self.end_time:
            self.end_time = self.time + timedelta(minutes=50)
        super().save(*args, **kwargs)
    

    
    
class Attendance(models.Model):
    """
    Models for Attendance
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    attendance = models.BooleanField(default=False)



class Parent(models.Model):
    """
    Models for Parent
    """
    name = models.CharField(max_length=200)
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    number = models.CharField(max_length=15)
    login_code = models.CharField(max_length=6, unique=True)  

    def __str__(self):
        return f"{self.name}"
    
    def save(self, *args, **kwargs):
        if not self.login_code:
            self.login_code = str(random.randint(100000, 999999))
        super().save(*args, **kwargs)



    