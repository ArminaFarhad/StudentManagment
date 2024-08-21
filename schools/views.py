import re
from urllib import request
from django.shortcuts import render, redirect
from django.contrib import messages
from schools.forms import SearchClass, Loginform
from django.contrib.auth.forms import AuthenticationForm
from .models import SchoolUser, Student, Subject, Grade, SubjectStudent, Teacher, User
from django.contrib import messages
from .models import Grade

def student_grades(request):
    grades = Grade.objects.filter(student=request.user)
    return render(request, 'students/grades.html', {'grades': grades})


def assign_grade(request):
        if request.method == 'POST':
            student_id = request.POST.get('student')
            subject_id = request.POST.get('subject')
            grade_value = request.POST.get('grade')

            teacher = request.POST.get('teacher_id')

            student = Student.objects.get(id=student_id)
            subject = Subject.objects.get(id=subject_id)

            Grade.objects.create(student=student, subject=subject, grade=grade_value)

            messages.success(request, 'Grade assigned successfully.')
            return GetTeachersSubjects(request)


def GetTeachersSubjects(request):
    if request.method == 'POST':
        user_id = request.POST.get('teacher_id')
        user = SchoolUser.objects.get(id = user_id)
        teacher = Teacher.objects.get(user_id=user.id)
        subjects = Subject.objects.filter(teacher_id=teacher.id)
        return render(request, 'teachers/subjects.html', {'subjects': subjects, 'teacher': teacher})
   

def GetSubjectStudents(request):
    if request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        
        subject = Subject.objects.get(id=subject_id)
        # Get all subject-student relationships for the given subject
        subject_students = SubjectStudent.objects.filter(subject=subject)
        student_ids = subject_students.values_list('students_id', flat=True)
        print(student_ids)
        # Get all students with the extracted IDs
        students = Student.objects.all()
        teacherid = request.POST.get('teacher_id')
        teacher = Teacher.objects.get(id = teacherid)
        print(students)
        return render(request, 'teachers/subjectStudents.html', {'students': students, 'teacher': teacher, 'subject': subject})
 
def loginTeacher(request):
    if request.method == 'POST':
        form = Loginform(request)
        teacher_username = form.request.POST.get('username')
        teacher_password = form.request.POST.get('password')
        user = SchoolUser.objects.get(username = teacher_username)
        if user.password == teacher_password and user.isteacher == True:
            request.user = user
            messages.success(request, f"Welcome, {teacher_username}! Your logged in successfully.")
            return render(request, 'teachers/profile.html')
    else:
        form = AuthenticationForm()
    return render(request, 'teachers/login.html', {'form': form})

def loginStudents(request):
    if (request.method == 'POST'):
        form = Loginform(request.POST)
        student_username = form.request.get('username')
        student_password = form.request.get('password')
        user = SchoolUser.objects.get(username = student_username)
        if user.password == student_password and user.isteacher == False:
            request.user = user
            student = Student.objects.get(user = user)
            grades = Grade.objects.filter(student = student)
            subjects = Subject.objects.filter(id__in = grades)
            
            return render(request, 'students/profile.html', {
                'student': student,
                'grades': grades
            })

            # messages.success(request, f"Welcome, {student_username}! Your logged in successfully.")
            # return render(request, 'students/profile.html')
    else:
        form = AuthenticationForm()
    return render(request, 'students/login.html', {'form': form})

