from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Payments)

class AppAdmin(admin.ModelAdmin):
    pass