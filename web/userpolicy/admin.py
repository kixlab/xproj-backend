from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import UserPolicy
# Register your models here.
admin.site.register(UserPolicy, SimpleHistoryAdmin)
