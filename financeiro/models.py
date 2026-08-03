from django.db import models
from clientes.models import Cliente
from atendimento.models import Atendimento
from agenda.models import Agendamento

STATUS_CHOICES = (
    ('PENDENTE', 'Pendente'),
    ('PAGO', 'Pago'),
    ('CANCELADO', 'Cancelado'),
)

class Lancamento(models.Model):
    # Campos que JÁ EXISTEM na migração 0001_initial:
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    atendimento = models.OneToOneField(Atendimento, on_delete=models.CASCADE, null=True, blank=True)
    data = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    forma_pagamento = models.CharField(max_length=30, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDENTE')

    # NOVOS CAMPOS (todos com null=True ou blank=True para permitir a criação da migração de forma limpa)
    agendamento = models.OneToOneField(
        Agendamento, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="lancamento"
    )
    descricao = models.CharField(max_length=255, blank=True, default='')
    data_vencimento = models.DateField(null=True, blank=True)
    
    criado_em = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    alterado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Lançamento #{self.id} - R$ {self.valor}"