from django.contrib import admin
from .models import Effect

# Register your models here.
class EffectAdmin(admin.ModelAdmin):
  readonly_fields = ('created',)

admin.site.register(Effect, EffectAdmin)