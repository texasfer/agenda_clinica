from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Empresa, Usuario


@admin.register(Usuario)
class CustomUsuarioAdmin(UserAdmin):
    # Removido 'empresa' da listagem e do filtro
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nome_fantasia', 'categoria', 'cor_primaria')
    search_fields = ('nome_fantasia',)
    list_filter = ('categoria',)