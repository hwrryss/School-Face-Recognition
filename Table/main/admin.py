from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Person


# Register your models here.

class PersonAdmin(UserAdmin):
    list_display = ('grade', 'name', 'time', 'status', 'reason')
    search_fields = ('name', )
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    ordering = ('name',)


admin.site.register(Person, PersonAdmin)
