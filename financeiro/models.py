from django.db import models
from atendimento.models import Atendimento


class Lancamento(models.Model):

    STATUS = [

        ("PENDENTE","Pendente"),
        ("PAGO","Pago"),

    ]

    atendimento = models.OneToOneField(
        Atendimento,
        on_delete=models.CASCADE
    )

    cliente = models.ForeignKey(
        "clientes.Cliente",
        on_delete=models.CASCADE
    )

    data = models.DateField()

    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    forma_pagamento = models.CharField(
        max_length=30,
        blank=True
    )

    status = models.CharField(
        max_length=15,
        choices=STATUS,
        default="PENDENTE"
    )

    def __str__(self):

        return self.cliente.nome