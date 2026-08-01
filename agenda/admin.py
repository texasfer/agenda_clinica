from django.contrib import admin
from .models import Agendamento


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):

    list_display = (
        "cliente",
        "profissional",
        "data",
        "hora_inicio",
        "hora_fim",
        "valor",
        "status",
    )

    search_fields = (
        "cliente__nome",
    )

    list_filter = (
        "status",
        "data",
        "profissional",
    )

    ordering = (
        "data",
        "hora_inicio",
    )

    list_per_page = 30