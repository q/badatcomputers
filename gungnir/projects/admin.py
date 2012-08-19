from django.contrib import admin
from django.db import models


app_name = 'projects'
app = models.get_app(app_name)
models = models.get_models(app)

for model in models:
    admin.site.register(model)