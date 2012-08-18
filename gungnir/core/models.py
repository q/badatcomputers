from django.db import models
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField

class BaseModel(models.Model):
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    class Meta:
        abstract = True
        get_latest_by = 'modified'