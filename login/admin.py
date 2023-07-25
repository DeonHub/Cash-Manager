from django.contrib import admin
from .models import *


# Register your models here.
@admin.register( ClientDetails, MemberDetails)

class AppAdmin(admin.ModelAdmin):
    pass
