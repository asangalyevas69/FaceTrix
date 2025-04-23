from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='students/')

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])

class Parent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

class Lesson(models.Model):
    subject = models.CharField(max_length=100)
    date = models.DateField()

