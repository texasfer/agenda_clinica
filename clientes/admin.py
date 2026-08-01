from django.contrib import admin
from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):

    list_display = (
        "nome",
        "telefone",
        "whatsapp",
        "cidade",
        "valor_sessao",
        "total_sessoes",
        "sessoes_realizadas",
        "sessoes_restantes",
        "status",
    )

    search_fields = (
        "nome",
        "cpf",
        "telefone",
        "whatsapp",
        "email",
    )

    list_filter = (
        "status",
        "cidade",
        "profissional",
    )

    ordering = (
        "nome",
    )

    list_per_page = 25