from django.contrib import admin
from .models import MiniSurvey
# Register your models here.

admin.site.register(MiniSurvey, admin.ModelAdmin)