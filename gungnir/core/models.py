from django.db import models
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class BaseModel(models.Model):
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    class Meta:
        abstract = True
        get_latest_by = 'modified'
        
class Profile(models.Model):
    user = models.OneToOneField(User)
    can_build = models.BooleanField(default=False, blank=True)
    aws_akey = models.CharField(max_length=64, blank=True)
    aws_skey = models.CharField(max_length=64, blank=True)
    
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.get_or_create(user=instance)
    post_save.connect(create_user_profile, sender=User)