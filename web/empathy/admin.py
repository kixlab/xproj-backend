from django.contrib import admin
from .models import Empathy

# Register your models here.
class EmpathyAdmin(admin.ModelAdmin):
  readonly_fields = ('created',)

admin.site.register(Empathy, EmpathyAdmin)