from django.db import models
from agenda.models import Agendamento


class Atendimento(models.Model):

    agendamento = models.OneToOneField(
        Agendamento,
        on_delete=models.CASCADE,
        related_name="atendimento"
    )

    queixa = models.TextField(blank=True)

    anamnese = models.TextField(blank=True)

    evolucao = models.TextField(blank=True)

    procedimentos = models.TextField(blank=True)

    conduta = models.TextField(blank=True)

    observacoes = models.TextField(blank=True)

    finalizado = models.BooleanField(default=False)

    criado_em = models.DateTimeField(auto_now_add=True)

    alterado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.agendamento.cliente.nome


