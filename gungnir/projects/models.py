from django.core.urlresolvers import reverse
from django.db import models
#from django_extensions.db.fields import SlugField
from gungnir.core.models import BaseModel

class Application(BaseModel):
    PROJECT_TYPE_CHOICES = (
        (0, 'Django'),
    )
    name = models.CharField(max_length=250)
    owner = models.ForeignKey('auth.User', related_name='applications')
    app_type = models.PositiveSmallIntegerField(choices=PROJECT_TYPE_CHOICES, default=0)

    def get_absolute_url(self):
        return reverse('gungnir-projects-application-detail', kwargs={'pk':self.pk})

class Repo(BaseModel):
    application = models.ForeignKey(Application, related_name='repos')
    url = models.CharField(max_length=2048)
    branch = models.CharField(max_length=50)
    # requirements

