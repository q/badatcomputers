from django.core.urlresolvers import reverse
from django.db import models
#from django_extensions.db.fields import SlugField
from gungnir.core.models import BaseModel


from git import Repo as GitRepo
#from gungnir.projects.tasks import fetch_repo_for_existing_entry
from celery.execute import send_task
from os import path

class Application(BaseModel):
    PROJECT_TYPE_CHOICES = (
        (0, 'Django'),
    )
    name = models.CharField(max_length=250)
    owner = models.ForeignKey('auth.User', related_name='applications')
    app_type = models.PositiveSmallIntegerField(choices=PROJECT_TYPE_CHOICES, default=0)

    def __unicode__(self):
        return u'{0}'.format(self.name)

    def get_absolute_url(self):
        return reverse('gungnir-projects-application-detail', kwargs={'pk':self.pk})

class Repo(BaseModel):
    application = models.ForeignKey(Application, related_name='repos')
    url = models.CharField(max_length=2048)
    branch = models.CharField(max_length=50, default='master')
    path_on_disk = models.CharField(max_length=1024)
    # requirements

    def repo_exists(self):
        """Determine if path_on_disk is a valid repo or not"""
        try:
            GitRepo(self.path_on_disk)
            return True

        except Exception as e:
            return False

    def branches(self):
        repo = GitRepo(self.path_on_disk)

        branches = list()
        for branch in repo.branches:
            branches.append(branch.name)

        return branches

    def save(self, *args, **kwargs):
        
        results = super(Application, self).save(*args, **kwargs)
        # Fire off a task to pull the repo and populate branch/path_on_disk, this should be done with a signal but i've had 8 hours sleep over hte past 40...
        send_task('gungnir.projects.tasks.fetch_repo_for_existing_entry', args=[self.repo_id])

        return results
