from django.contrib import admin
from .models import Category, Person, Promise, BudgetProgram

admin.site.register(Category, admin.ModelAdmin)

admin.site.register(Person, admin.ModelAdmin)

class PromiseAdmin(admin.ModelAdmin):
    model = Promise
    list_display = ('title', 'categories',)
admin.site.register(Promise, PromiseAdmin)

class PersonInline(admin.TabularInline):
    model = Person
    fields = ('name',)
    readonly_fields = ('name',)
    can_delete = False
    show_change_link = True

admin.site.register(BudgetProgram, admin.ModelAdmin)