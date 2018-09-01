from django.contrib import admin
from .models import Flag

# Register your models here.
class FlagAdmin(admin.ModelAdmin):
  readonly_fields = ('created',)

admin.site.register(Flag, FlagAdmin)