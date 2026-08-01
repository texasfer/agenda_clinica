from django.contrib import admin
from .models import Recibo


@admin.register(Recibo)
class ReciboAdmin(admin.ModelAdmin):

    list_display = (

        "numero",

        "data",

        "valor",

        "enviado_email",

    )

    ordering = ("-numero",)