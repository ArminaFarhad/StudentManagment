from pyclbr import Class
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Subject, Teacher, Student

class Loginform(AuthenticationForm):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(max_length=100, required=True)

class SearchClass(forms.Form):
    Subject = forms.CharField(max_length=100, required=True)
    Teacher = forms.CharField(max_length=100, required=True)


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    is_teacher = forms.BooleanField(required=False, label="Sign up as a Teacher")
    subject = forms.CharField(max_length=100, required=False, help_text="Required for teachers")
    grade_level = forms.CharField(max_length=10, required=False, help_text="Required for students")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

            if self.cleaned_data['is_teacher']:
                Teacher.objects.create(user=user, subject=self.cleaned_data['subject'])
            else:
                Student.objects.create(user=user, grade_level=self.cleaned_data['grade_level'])

        return user
