from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import User

ADDITIONAL_USER_FIELDS = (
    (None, {'fields': ('year_of_birth', 'location', )}),
)

class MyUserAdmin(UserAdmin):
    model = User
    raw_id_fields = ("location",)

    add_fieldsets = UserAdmin.add_fieldsets + ADDITIONAL_USER_FIELDS
    fieldsets = UserAdmin.fieldsets + ADDITIONAL_USER_FIELDS

admin.site.register(User, MyUserAdmin)