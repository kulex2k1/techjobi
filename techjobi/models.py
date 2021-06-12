from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.fields import TextField
from django.forms.widgets import Textarea


class JobPost(models.Model):
    job_title = models.CharField(max_length=255, blank=True)

    job_type_choices = [
        ('Full Time', 'Full Time'),
        # ('Freelance', 'Freelance'),
        ('Part Time', 'Part Time'),
        ('Temporary', 'Temporary'),
        
    ]
    job_type = models.CharField(
        max_length=50,
        choices=job_type_choices  
    )
    
    job_category_choices = [
        ('Hardware', 'Hardware'),
        ('Software/Web Development', 'Software/Web Development'),
        ('Data Science', 'Data Science'),
        ('Product Development-digital banking', 'Product development-digital banking'),
        ('Process ', 'Process'),
        ('Support specialist', 'Support specialist'),
      

        # ('Web & Software Dev', 'Web & Software Dev'),
        # ('Data Science & Analitycs', 'Data Science & Analitycs'),
        # ('Networking', 'Networking'),
        # ('Support specialist', 'Support specialist'),
        # ('Software Testing', 'Software Testing'),
        # ('Analyst', 'Analyst'),
        # ('User experience designer', 'User experience designer'),


        
    ]
    job_category = models.CharField(
        max_length=100,
        choices=job_category_choices  
    )

    company_name = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    salary1 = models.FloatField(blank=True)
    salary2 = models.FloatField(blank=True)
    tags = models.CharField(max_length=255, blank=True)
    job_description = models.TextField( blank=True)
    file_upload = models.FileField(blank=True)

    status_choices = [

        ('Approved', 'Approved'),
        ('Expired', 'Expired'),
        
    ]
    status = models.CharField(
        max_length=50,
        default= 'Pending Approval',
        blank=True,
        choices=status_choices  
    )
    deadline = models.DateField(null=True, blank=True )
    entry_date = models.DateField(auto_now_add=True )
    update_date = models.DateField(auto_now=True)
    class Meta:
        db_table = 'post'


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=CASCADE)
    username = models.CharField(max_length=255, blank=True, unique=True)
    profile_pic = models.ImageField(blank=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=254, blank=True)

    skills = models.CharField(max_length=255, blank=True)
    nationality = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True)
    account_type = models.CharField(max_length=255, blank=True)

    job_role = models.CharField(max_length=255, blank=True)
    company = models.CharField(max_length=255, blank=True)
    start_period = models.CharField(max_length=255, blank=True)
    end_period = models.CharField(max_length=255, blank=True)
    duty = models.TextField(blank=True)

    doc_upload = models.FileField(blank=True)
    tag = models.CharField(max_length=255, blank=True)
    intro = models.TextField(blank=True)
    company_view = models.IntegerField(blank=True, default=0)
    application_view = models.IntegerField(blank=True, default=0)

    entry_date = models.DateField(auto_now_add=True )
    update_date = models.DateField(auto_now=True)

    class Meta:
        db_table = 'profile'



class Company(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=CASCADE)
    username = models.CharField(max_length=255, blank=True)

    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    company_email = models.CharField(max_length=255, blank=True)
    account_type = models.CharField(max_length=255, blank=True)

    company_name = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    company_description = models.TextField( blank=True)
    file_upload = models.FileField(blank=True)
    entry_date = models.DateField(auto_now_add=True )
    update_date = models.DateField(auto_now=True)
    class Meta:
        db_table = 'company'
        

class Employement(models.Model):
    job_role1 = models.CharField(max_length=255, blank=True)
    company1 = models.CharField(max_length=255, blank=True)
    period1a = models.DateField(null=True, blank=True )
    period1b = models.DateField(auto_now_add=True )
    duty1 = models.TextField(blank=True)

    class Meta:
        db_table = 'employment'


class Application(models.Model):
    job_post = models.CharField(max_length=255, blank=True)
    username = models.CharField(max_length=255, blank=True)
    job_title = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    deadline = models.DateField(null=True, blank=True )
    company_name = models.CharField(max_length=255, blank=True)
    entry_date = models.DateField(auto_now_add=True )
    
    class Meta:
        db_table = 'applications'

    
class Notes(models.Model):
    username = models.CharField(max_length=255, blank=True)
    priority_choices = [
        ('Low Priority', 'Low Priority'),
        ('Medium Priority', 'Medium Priority'),
        ('Medium Priority', 'Medium Priority'),    
    ]
    priority = models.CharField(
        max_length=50,
        choices=priority_choices  
    )
    
    note = models.TextField(blank=True)
    entry_date = models.DateField(auto_now_add=True )
    update_date = models.DateField(auto_now=True)

    class Meta:
        db_table = 'notes'