from django.contrib import admin
from .models import Fishy

# Register your models here.
class FishyAdmin(admin.ModelAdmin):
  readonly_fields = ('created',)

admin.site.register(Fishy, FishyAdmin)