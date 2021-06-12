from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group

from .import views

def candidate_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='employer')
        instance.groups.add(group)
        
        

post_save.connect(candidate_profile, sender=User)