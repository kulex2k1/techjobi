from django import forms
from django.forms import ModelForm 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import JobPost, Profile, Company,Employement, Application, Notes

class PostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = '__all__'


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude =['nationality', 'account_type', 'hourly_rate', 'user', 'username', 'application_view', 'company_view']


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields=['username', 'email', 'password1', 'password2']


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'
        exclude =[ 'account_type', 'user']

class EmployementForm(forms.ModelForm):
    class Meta:
        model = Employement
        fields = '__all__'


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = '__all__'


class NoteForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = '__all__'
