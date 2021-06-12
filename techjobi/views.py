from django.core import exceptions
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import unauthenticated_user, allowerd_users
from .models import JobPost, Profile, Company, Employement, Application, Notes
from .forms import NoteForm, PostForm, ProfileForm, RegistrationForm, CompanyForm, EmployementForm, ApplicationForm
from django.contrib.auth.forms import UserCreationForm 
from django.core.exceptions import ObjectDoesNotExist
from datetime import date
from django.core.mail import EmailMessage
from django.template.loader import get_template
today = date.today()

# Create your views here.
@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        username = username.capitalize()
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
  
            login(request, user)
            return redirect('home') 
    context ={}
    return render(request, 'job/pages-login.html', context)



def logoutPage(request):
    logout(request)
    messages.success(request, 'You have been logged out, Succesfully!')
    return redirect('index')



@unauthenticated_user
def registerPage(request):
    form2 =  RegistrationForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        username = username.capitalize()
      
        form = RegistrationForm(request.POST)
        form2 = RegistrationForm(request.POST)
        if form.is_valid():
            reg = form2.save()
           
            reg.username = username
            reg.save()
            return redirect('login')
    context = {"form2":form2}
    return render(request, 'job/pages-register.html', context)

import requests    
@unauthenticated_user
def index(request):
    # html_content = get_template("email/registration.html")
    # html_content = html_content.render(context = {})
    # msg = EmailMessage('TechJobi Registration Successful', html_content, 'app.notifications@ubagroup.com', ['kolawobee@gmail.com']) 
    # msg.content_subtype = "html"
    # msg.send()

    form2 =  RegistrationForm()
    if request.method == 'POST' and 'regist' in request.POST:
        username = request.POST.get('username')
        email = request.POST.get('email')
        register = request.POST.get('account-type-radio')   
        username = username.capitalize()
        form = RegistrationForm(request.POST)
        form2 = RegistrationForm(request.POST)
        if form.is_valid():
            reg = form2.save()
            reg.username = username
            reg.account_type = register
            reg.save()
            if register == 'candidate':
                user_group = Group.objects.get(name='candidate') 
                reg.groups.add(user_group)
                Profile.objects.create(
                    user=reg,
                    account_type = 'candidate',
                    email = email,
                    username = username,
                )
                html_content = get_template("email/registration.html")
                html_content = html_content.render(context = {'username':username})
                msg = EmailMessage('TechJobi Registration Successful', html_content, 'app.notifications@ubagroup.com', [email]) 
                msg.content_subtype = "html"
                msg.send(fail_silently=False)
                messages.success(request, 'Registration was Successful; Please Log In!')
                return redirect('index')
            else:
            
                user_group = Group.objects.get(name='employer') 
                reg.groups.add(user_group)   
                Company.objects.create(
                    user=reg,
                    account_type = 'employer',
                    email = email,
                    username = username,
                
                )                  
                html_content = get_template("email/registration.html")
                html_content = html_content.render(context = {'username':username})
                msg = EmailMessage('TechJobi Registration Successful', html_content, 'app.notifications@ubagroup.com', [email]) 
                msg.content_subtype = "html"
                msg.send(fail_silently=False)
                messages.success(request, 'Registration was Successful; Please Log In!')
                return redirect('index')
        
                
    elif request.method == 'POST' and 'log-in' in request.POST:
        username = request.POST.get('username')
        username = username.capitalize()
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            #messages.success(request, 'Welcome '+username)
            return redirect('home')
        else:
            messages.error(request, 'Wrong Username or Password')
    
    
    
    elif request.method == 'POST' and 'log-in' not in request.POST and 'regist' not in request.POST:
        job_location = request.POST.get('job_location')
        job_type = request.POST.get('job_type')
        job_listings1 = JobPost.objects.filter(job_title__iexact=job_type)
        job_listings2 = JobPost.objects.filter(job_title__icontains=job_type)
        job_listings3 = JobPost.objects.filter(location__iexact=job_location)
        job_listings4 = JobPost.objects.filter(location__icontains=job_location)
        job_listings = job_listings2 | job_listings1 | job_listings3 | job_listings4
        global val_id
        def val_id():
            return job_listings
        
        return redirect('job_list_unreg')

    context = {"form2":form2}
    return render(request, 'job/index-logged-out.html', context)



val_id=None
@login_required(login_url  ='index')
def home(request): 
    company_details = ''
    username = str(request.user)
    try:
        details = Profile.objects.get(username=username)
    except ObjectDoesNotExist:
        company_details = Company.objects.get(username=username)
    account_type = details.account_type
    
    if details.first_name == '' :
        if details.account_type == 'candidate':
            messages.info(request, 'Welcome ' + username +', Please Update your Profile to proceed')
            return redirect('profile_settings')
    elif details.first_name != '':
        if details.account_type == 'employer':
            details = Profile.objects.get(username=username)
    elif details.first_name != '':
        if details.account_type == 'candidate':
            details = Profile.objects.get(username=username)
    elif company_details.first_name == '':
        if company_details.account_type == 'employer':
            messages.info(request, 'Welcome ' + username +', Please Update your Profile to proceed')
            return redirect('employer_settings')

    employees = Profile.objects.all().count()
    job_posted = JobPost.objects.all().count()
    top_job = JobPost.objects.all().order_by('-id')[:5]
    abuja = JobPost.objects.filter(location__iexact='abuja').count()
    enugu = JobPost.objects.filter(location__iexact='enugu').count()
    oyo = JobPost.objects.filter(location__iexact='oyo').count()
    lagos = JobPost.objects.filter(location__iexact='lagos').count()
    if request.method == 'POST':
        job_location = request.POST.get('job_location')
        job_type = request.POST.get('job_type')
        job_listings1 = JobPost.objects.filter(job_title__iexact=job_type)
        job_listings2 = JobPost.objects.filter(job_title__icontains=job_type)
        job_listings3 = JobPost.objects.filter(location__iexact=job_location)
        job_listings4 = JobPost.objects.filter(location__icontains=job_location)
        job_listings = job_listings2 | job_listings1 | job_listings3 | job_listings4
        global val_id
        def val_id():
            return job_listings
        
        return redirect('job_list')
    context = {"employees":employees, "account_type":account_type, "job_posted":job_posted,"top_job":top_job, "today":today, "oyo":oyo, "enugu":enugu, "lagos":lagos, "abuja":abuja}
    return render(request, 'base/index.html', context)




val_id=None
@login_required(login_url  ='index')
def job_search(request): 
    if request.method == 'GET':
        job_listings = JobPost.objects.all()
    if request.method == 'POST':
        job_location = request.POST.get('job_location')
        job_type = request.POST.get('job_type')
        job_listings1 = JobPost.objects.filter(job_title__iexact=job_type)
        job_listings2 = JobPost.objects.filter(job_title__icontains=job_type)
        job_listings3 = JobPost.objects.filter(location__iexact=job_location)
        job_listings4 = JobPost.objects.filter(location__icontains=job_location)
        job_listings = job_listings2 | job_listings1 | job_listings3 | job_listings4
        global val_id
        def val_id():
            return job_listings
        return redirect('job_list')
    
    context = {"job_listings":job_listings, "today":today}
    return render(request, 'job/jobs-list-layout-1.html', context)



def job_list(request):
    job_listings = val_id()
    if request.method == 'GET':
        job_listings = val_id()
    if request.method == 'POST':
        job_location = request.POST.get('job_location')
        job_type = request.POST.get('job_type')
        job_listings1 = JobPost.objects.filter(job_title__iexact=job_type)
        job_listings2 = JobPost.objects.filter(job_title__icontains=job_type)
        job_listings3 = JobPost.objects.filter(location__iexact=job_location)
        job_listings4 = JobPost.objects.filter(location__icontains=job_location)
        job_listings = job_listings2 | job_listings1 | job_listings3 | job_listings4
        for job in job_listings:
            print(job)
        
   
        
        #context = {"job_posted":job_posted}
    context = {"job_listings":job_listings, "today":today}
    return render(request, 'job/jobs-list-layout-1.html', context)


@unauthenticated_user
def job_list_unreg(request):
    form2 =  RegistrationForm()
    job_listings = val_id()
    if request.method == 'GET':
        job_listings = val_id()
    if request.method == 'POST' and 'log-in' not in request.POST and 'regist' not in request.POST:
        job_location = request.POST.get('job_location')
        job_type = request.POST.get('job_type')
        job_listings1 = JobPost.objects.filter(job_title__iexact=job_type)
        job_listings2 = JobPost.objects.filter(job_title__icontains=job_type)
        job_listings3 = JobPost.objects.filter(location__iexact=job_location)
        job_listings4 = JobPost.objects.filter(location__icontains=job_location)
        job_listings = job_listings2 | job_listings1 | job_listings3 | job_listings4
    
    elif request.method == 'POST' and 'regist' in request.POST:
        username = request.POST.get('username')
        username = username.capitalize()
        form = RegistrationForm(request.POST)
        form2 = RegistrationForm(request.POST)
        if form.is_valid():
            reg = form2.save()
            reg.username = username
            reg.save()
            messages.success(request, 'Registration Successful, Please Log in')
            return redirect('index')
    elif request.method == 'POST' and 'log-in' in request.POST:

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')    
   
        
        #context = {"job_posted":job_posted}
    context = {"job_listings":job_listings, "today":today, "form2":form2}
    return render(request, 'job/jobs-list-layout-2.html', context)


@login_required(login_url  ='index')
def employee_list(request):
    if request.method == 'GET':
        employee_listings = []
    if request.method == 'POST':
        employee_location = request.POST.get('employee_location')
        
        job_type = request.POST.get('job_type')
        employee_listings1 = Profile.objects.filter(skills__iexact=job_type).filter(account_type='candidate')
        employee_listings2 = Profile.objects.filter(skills__icontains=job_type).filter(account_type='candidate')
        employee_listings3 = Profile.objects.filter(location__iexact=employee_location).filter(account_type='candidate')
        employee_listings4 = Profile.objects.filter(location__icontains=employee_location).filter(account_type='candidate')
        employee_listings = employee_listings1 | employee_listings2 | employee_listings3 | employee_listings4
        print(employee_listings)
        
   
        
        #context = {"job_posted":job_posted}
    context = {"employee_listings":employee_listings, "today":today}

    return render(request, 'job/freelancers-list-layout-1.html', context)

@login_required(login_url  ='index')
def company_list(request):
    
    context = {}
    return render(request, 'job/browse-companies.html', context)

@login_required(login_url  ='index')
def task_list(request):
    
    context = {}
    return render(request, 'job/tasks-list-layout-1.html', context)

@login_required(login_url  ='index')
def post_job(request):
    username = request.user
    username = str(username)
    companys = Company.objects.get(username=username)
    company_name = companys.company_name

    form  = PostForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        form = PostForm(request.POST , request.FILES)
        if form.is_valid:
            posts = form.save()
            posts.company_name = company_name
            posts.save()
            return redirect('dashboard')

    form  = PostForm()
    context = {"form":form, "company_name":company_name}
    return render(request, 'job/dashboard-post-a-job.html', context)


@login_required(login_url  ='index')
def post_task(request):
    
    context = {}
    return render(request, 'job/dashboard-post-a-task.html', context)


@login_required(login_url  ='index')
def dashboard(request):
    username = request.user
    username = str(username)
    jobs_count =  Application.objects.filter(username=username).count()
    view_count =  Profile.objects.get(username=username)
    application_view  = view_count.application_view
    company_view  = view_count.company_view
    note_stat = Notes.objects.filter(username=username)
    
    if request.method == 'POST':
        note = request.POST.get('note')
        priority = request.POST.get('priority')
        a = Notes(username=username,  priority=priority, note=note)
        a.save()
        messages.success(request, 'Note successfully added')
        
    
    form = NoteForm()
    context = {"jobs_count":jobs_count, "company_view":company_view, "application_view":application_view, "note_stat":note_stat }
    return render(request, 'job/dashboard.html', context)




@login_required(login_url  ='index')
def job_page(request, pk): 
    viewer = request.user
    viewer= str(viewer)
    count = Profile.objects.get(username='Obiora')
    application_view = count.application_view
    count.application_view = count.application_view + 1
    count.save()
 
    job_details = JobPost.objects.get(id = pk)
    job_id = job_details.id
    form = PostForm(instance = job_details)
    form2 = ApplicationForm()
    
    if request.method == 'POST':
        try:
            details = Application.objects.filter(username=viewer).filter(job_post = job_id).count()
            if details > 0:
                print('okay')
                messages.success(request, 'You have already applied for this job!')
                return redirect('dashboard')
        except ObjectDoesNotExist:
            details = None

        form2 = ApplicationForm(request.POST)
        if form.is_valid:
            job_apply = form2.save()
            job_apply.username = viewer
            job_apply.job_post = job_details.id
            job_apply.job_title = job_details.job_title
            job_apply.location = job_details.location
            job_apply.company_name = job_details.company_name
            job_apply.save()
            messages.success(request, 'Application successful')
            return redirect('dashboard')
    context = {"job_details":job_details, "today":today , "form2":form2, "application_view":application_view}
    return render(request, 'job/single-job-page.html', context)



@login_required(login_url  ='index')
def task_page(request):
    
    context = {}
    return render(request, 'job/single-task-page.html', context)

@login_required(login_url  ='index')
def profile_settings(request):
    username = str(request.user)
    details = Profile.objects.get(username=username)
    form  = ProfileForm(instance=details)
    first_name = details.first_name
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=details)
        nationality = request.POST.get('nationality')
        if form.is_valid:
            print(form)
            profile2 = form.save()
            
            profile2.nationality = nationality
    
            profile2.save()
            return redirect('dashboard')

    context = {"form":form,  "details":details, "first_name":first_name}
    return render(request, 'job/dashboard-settings.html', context)



@login_required(login_url  ='index')
def employer_settings(request):
    username = str(request.user)
    try:
        details = Company.objects.get(username=username)
        first_name = details.first_name
    except ObjectDoesNotExist:
        details = None
        first_name = ''
    form  = CompanyForm(request.POST or None, request.FILES or None, instance=details)
    if request.method == 'POST':
        print(form)
        form = CompanyForm(request.POST , request.FILES, instance=details)
        if form.is_valid:
            employ=form.save()
            employ.username = username
            employ.save()
            return redirect('dashboard')
    context = {"form":form, "details":details, "first_name":first_name}
    return render(request, 'job/employer-settings.html', context)

company_listings = []
def company_list(request):
    if request.method == 'GET':
        company_listings = Company.objects.all().order_by('id')[:6]
    else:
        company_name = request.POST.get('company_name')
        company_listings1 = Company.objects.filter(company_name__iexact=company_name)
        company_listings2 = Company.objects.filter(company_name__icontains=company_name)
        # company_listings3 = JobPost.objects.filter(location__iexact=company_location)
        # company_listings4 = JobPost.objects.filter(location__icontains=company_location)
        company_listings = company_listings1 | company_listings2 
       
        #context = {"job_posted":job_posted}
    context = {"company_listings":company_listings}
    return render(request, 'job/browse-companies.html', context)



@login_required(login_url ='index')
def company_profile(request, pk):
    viewer = request.user

    count = Profile.objects.get(username='Obiora')
    company_view = count.company_view
    count.company_view = count.company_view + 1
    count.save()
    company_details = Company.objects.get(id = pk)
    company_name = company_details.company_name
    posts = JobPost.objects.filter(company_name = company_name)
    form = PostForm(instance = company_details)
    
    context = {"company_details":company_details, "today":today, "posts":posts }
    return render(request, 'job/single-company-profile.html', context)


@login_required(login_url ='index')
def employee_profile(request, pk):
    viewer = request.user
    employee_details = Profile.objects.get(id = pk)
    #form = PostForm(instance = company_details)
    context = {"employee_details":employee_details, "today":today }
    return render(request, 'job/single-freelancer-profile.html', context)


@login_required(login_url ='index')
def job_applied(request, pk):
    username = request.user
    details = Application.objects.filter(username=username)

   # job_details = JobPost.objects.get(id=job_id.job_post)

  
    context = {"details":details, "details":details}
    return render(request, 'job/dashboard-my-active-jobs.html', context)



@login_required(login_url ='index')
def manage_job(request):
    username = request.user
    #details = Application.objects.filter(username=username)
    company_details = Company.objects.get(username=username)
    company_name = company_details.company_name
    job_details = JobPost.objects.filter(company_name=company_name)
    # for jobs in job_details:
    #     applicants = Application.objects.filter(job_title=jobs.job_title)
    #     for app in applicants:
    #         print(app)

    
 

  
    context = {"job_details":job_details}
    return render(request, 'job/dashboard-manage-jobs.html', context)



def edit_note(request, pk):
    username = request.user
    note_stat = Notes.objects.get(id=pk)
    
    if request.method == 'POST':
        note = request.POST.get('note')
        priority = request.POST.get('priority')
        a = Notes.objects.get(id=pk)
        a.note = note
        a.priority = priority
        a.save()
        messages.success(request, 'Note updated successful ')
        return redirect('dashboard')
    context = {"note_stat":note_stat}
    return render(request, 'job/dashboard2.html', context)




def delete_note(request, pk):
    username = request.user
    a= Notes.objects.filter(id= pk)
    a.delete()
    messages.success(request, 'Note has been successfully deleted!')
    return redirect('dashboard')



@login_required(login_url ='index')
def manage_candidate(request):
    username = request.user
    #details = Application.objects.all(username=username)
    # company_details = Company.objects.get(username=username)
    # company_name = company_details.company_name
    # job_details = JobPost.objects.filter(company_name=company_name)

  
    context = {}
    return render(request, 'job/dashboard-manage-candidates.html', context)


@login_required(login_url ='index')
def job_posted(request):
    filed = 'job_posted'
    username = request.user
    company = Company.objects.get(username=username)
    details = JobPost.objects.filter(company_name=company.company_name)

  
    context = {"details":details, "filed":filed}
    return render(request, 'job/dashboard-my-active-jobs.html', context)