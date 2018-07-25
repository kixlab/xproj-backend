from django.contrib import admin
from .models import Effect

# Register your models here.

admin.site.register(Effect, admin.ModelAdmin)