from django.contrib import admin
from .models import UserPolicy
# Register your models here.
admin.site.register(UserPolicy, admin.ModelAdmin)
