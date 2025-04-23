from django.db import models


class Group(models.Model):
    group_name = models.CharField(max_length=50)

    def __str__(self):
        return self.group_name


class Student(models.Model):
    full_name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='faces/')
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name
    


class Teacher(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


    
class Lesson(models.Model):
    subject_name = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.subject_name}-{self.time}"
    
    
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    attendance = models.BooleanField(default=False)



class Parent(models.Model):
    name = models.CharField(max_length=200)
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.name}"



    