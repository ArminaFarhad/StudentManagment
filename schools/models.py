from operator import truediv
from pyexpat import model
import time
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class SchoolUser(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    name = models.CharField(max_length=100, null=True)
    mobile = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    isteacher = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.username
    
    
class Teacher(models.Model):
    user = models.OneToOneField(SchoolUser, on_delete=models.CASCADE)
    subjects = models.ManyToManyField('Subject', related_name='taught_by')  

    def __str__(self):
        return f"{self.user.username} - Teacher"

class Student(models.Model):
    user = models.OneToOneField(SchoolUser, on_delete=models.CASCADE)
    grade_level = models.CharField(default=1, max_length=10)

    def __str__(self):
        return self.user.name

class Subject(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teachers')  

    def __str__(self):
        return self.name

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.IntegerField()
    date_assigned = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return f"{self.student.user.username} - {self.subject.name}: {self.grade}"



class SubjectStudent(models.Model):
    subject = models.ForeignKey(Subject, on_delete= models.CASCADE)
    students = models.ForeignKey(Student, on_delete= models.CASCADE)
    classtime = models.DateTimeField(null=True)
    teacher= models.ForeignKey(Teacher, on_delete= models.CASCADE, null=True)

    def __str__(self) -> str:
        return self.subject.name