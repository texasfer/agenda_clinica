from django.db import models
from clientes.models import Cliente
from usuarios.models import Usuario


class Agendamento(models.Model):

    STATUS = [
        ("AGENDADO", "Agendado"),
        ("CONFIRMADO", "Confirmado"),
        ("ATENDIMENTO", "Em Atendimento"),
        ("ATENDIDO", "Atendido"),
        ("CANCELADO", "Cancelado"),
        ("FALTOU", "Faltou"),
        ("REMARCADO", "Remarcado"),
    ]

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name="agendamentos"
    )

    profissional = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    data = models.DateField()

    hora_inicio = models.TimeField()

    hora_fim = models.TimeField()

    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    observacoes = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="AGENDADO"
    )

    criado_em = models.DateTimeField(auto_now_add=True)

    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["data", "hora_inicio"]

    def __str__(self):
        return f"{self.cliente} - {self.data}"