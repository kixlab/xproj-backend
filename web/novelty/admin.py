from django.contrib import admin
from .models import Novelty

# Register your models here.
class NoveltyAdmin(admin.ModelAdmin):
  readonly_fields = ('created',)

admin.site.register(Novelty, NoveltyAdmin)