from django.contrib import admin
from .models import Persons,Groups

# Register your models here.
admin.site.register(Persons)
admin.site.register(Groups)