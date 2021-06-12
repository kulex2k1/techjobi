from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import unauthenticated_user, allowerd_users
from .models import JobPost, Profile
from .forms import PostForm, ProfileForm, RegistrationForm
from django.contrib.auth.forms import UserCreationForm 
from datetime import date
today = date.today()

# Create your views here.
@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
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

@unauthenticated_user
def index(request):
    form2 =  RegistrationForm()
    if request.method == 'POST' and 'regist' in request.POST:
        username = request.POST.get('username')
        register = request.POST.get('account-type-radio')
        
        username = username.capitalize()
        form = RegistrationForm(request.POST)
        form2 = RegistrationForm(request.POST)

        if form.is_valid():
            reg = form2.save()
            reg.username = username
            reg.save()
            print(register)
            if register == 'candidates':
                user_group = Group.objects.get(name='candidates') 
                reg.groups.add(user_group)
                #login(request, user)
                messages.success(request, 'Welcome ' + username +'  Your Registration was Successfull; You have been Logged In!')
                return redirect('index')
            else:
                print(register)
                user_group = Group.objects.get(name='employer') 
                reg.groups.add(user_group)                     
                #login(request, user)
                messages.success(request, 'Welcome ' + username +'  Your Registration was Successfull; Please Log In!')
                return redirect('index')
                # messages.success(request, 'Registration Successfull, Please Log in')
                # return redirect('index')

    elif request.method == 'POST' and 'log-in' in request.POST:
        username = request.POST.get('username')
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
        job_listings4 = JobPost.objects.filter(location__icontains=job_type)
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
        job_listings4 = JobPost.objects.filter(location__icontains=job_type)
        job_listings = job_listings2 | job_listings1 | job_listings3 | job_listings4
        global val_id
        def val_id():
            return job_listings
        
        return redirect('job_list')
    context = {"job_posted":job_posted,"top_job":top_job, "today":today, "oyo":oyo, "enugu":enugu, "lagos":lagos, "abuja":abuja}
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
        job_listings4 = JobPost.objects.filter(location__icontains=job_type)
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
        job_listings4 = JobPost.objects.filter(location__icontains=job_type)
        job_listings = job_listings2 | job_listings1 | job_listings3 | job_listings4
        
   
        
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
        job_listings4 = JobPost.objects.filter(location__icontains=job_type)
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
            messages.success(request, 'Registration Successfull, Please Log in')
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
def freelancer_list(request):
    
    context = {}
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
    company_name = request.user
    company_name = str(company_name)
    
    form  = PostForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        form = PostForm(request.POST , request.FILES)
        if form.is_valid:
            posts = form.save()
            posts.company = company_name
            posts.save()
            return redirect('home')

    form  = PostForm()
    context = {"form":form, "company_name":company_name}
    return render(request, 'job/dashboard-post-a-job.html', context)


@login_required(login_url  ='index')
def post_task(request):
    
    context = {}
    return render(request, 'job/dashboard-post-a-task.html', context)


@login_required(login_url  ='index')
def dashboard(request):
    
    context = {}
    return render(request, 'job/dashboard.html', context)

@login_required(login_url  ='index')
def job_page(request, pk):
    viewer = request.user
    job_details = JobPost.objects.get(id = pk)
    
    form = PostForm(instance = job_details)
    

    
    context = {"job_details":job_details, "today":today }
    return render(request, 'job/single-job-page.html', context)

@login_required(login_url  ='index')
def task_page(request):
    
    context = {}
    return render(request, 'job/single-task-page.html', context)

@login_required(login_url  ='index')
def profile_settings(request):
    form  = ProfileForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        form = ProfileForm(request.POST , request.FILES)
        nationality = request.POST.get('nationality')
        hourly_rate = request.POST.get('hourly_rate')
        if form.is_valid:
            profile = form.save()
            profile.nationality = nationality
            profile.hourly_rate = hourly_rate
            profile.save()
            return redirect('home')
    form  = ProfileForm()
    context = {"form":form}
    return render(request, 'job/dashboard-settings.html', context)