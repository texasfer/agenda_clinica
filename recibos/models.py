from django.db import models
from financeiro.models import Lancamento


class Recibo(models.Model):

    lancamento = models.OneToOneField(
        Lancamento,
        on_delete=models.CASCADE,
        related_name="recibo"
    )

    numero = models.PositiveIntegerField(unique=True)

    data = models.DateField(auto_now_add=True)

    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    observacao = models.TextField(blank=True)

    enviado_email = models.BooleanField(default=False)

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"Recibo {self.numero}"