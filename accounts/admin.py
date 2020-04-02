from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from covid19.models import Usuario

admin.site.register(Usuario, UserAdmin)