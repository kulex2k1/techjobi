"""Itjobs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('job-list/', views.job_list, name='job_list'),
    path('register/', views.registerPage, name='register'),
    path('employee-list/', views.employee_list, name='employee_list'),
    path('company-list/', views.company_list, name='company_list'),
    path('task-list/', views.task_list, name='task_list'),
    path('post-job/', views.post_job, name='post_job'),
    path('post-task/', views.post_task, name='post_task'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('job-page/<str:pk>/', views.job_page, name='job_page'),
    path('task-page/', views.task_page, name='task_page'),
    path('profile-settings/', views.profile_settings, name='profile_settings'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('company-profile/<str:pk>/', views.company_profile, name='company_profile'),
    path('employer-settings/', views.employer_settings, name='employer_settings'),
    path('job-search/', views.job_search, name='job_search'),
    path('job-search-list/', views.job_list_unreg, name='job_list_unreg'),
    path('employee-profile/<str:pk>/', views.employee_profile, name='employee_profile'),
    path('applied-job/<str:pk>/', views.job_applied, name='job_applied'),
    path('manage-job/', views.manage_job, name='manage_job'),
    path('edit-note/<str:pk>/', views.edit_note, name='edit_note'),
    path('delete-note/<str:pk>/', views.delete_note, name='delete_note'),
    path('manage-candidate/', views.manage_candidate, name='manage_candidate'),
    path('jobs-posted/', views.job_posted, name='job_posted'),
]