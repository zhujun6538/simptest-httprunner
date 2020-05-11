from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Teststep)
admin.site.register(models.Variables)
admin.site.register(models.Validates)
admin.site.register(models.Headers)
admin.site.register(models.Extracts)
admin.site.register(models.TestSuite)
admin.site.register(models.TestCase)