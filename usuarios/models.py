from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):

    PERFIS = [

        ("SUPER", "Super Administrador"),
        ("ADMIN", "Administrador"),
        ("PROF", "Profissional"),
        ("RECEP", "Recepção"),

    ]

    perfil = models.CharField(
        max_length=10,
        choices=PERFIS,
        default="PROF"
    )

    telefone = models.CharField(
        max_length=20,
        blank=True
    )

    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.get_full_name() or self.username

    from django.db import models

class Empresa(models.Model):
    CATEGORIA_CHOICES = [
        ('GERAL', 'Multidisciplinar / Geral'),
        ('MENTAL', 'Saúde Mental (Psicologia/Psiquiatria)'),
        ('FISICA', 'Saúde Física (Fisioterapia/Ortopedia)'),
        ('SOCIAL', 'Bem-Estar Social / Familiar'),
        ('ODONTO', 'Odontologia / Estética'),
        ('NUTRICAO', 'Nutrição / Acompanhamento'),
    ]

    nome_fantasia = models.CharField(max_length=100)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, default='GERAL')
    logo_personalizado = models.ImageField(upload_to='logos_clinicas/', null=True, blank=True)
    cor_primaria = models.CharField(max_length=7, blank=True, help_text="Exemplo: #0284C7")

    def __str__(self):
        return self.nome_fantasia

    @property
    def cor_tema(self):
        if self.cor_primaria:
            return self.cor_primaria
        
        mapa_cores = {
            'GERAL': '#0284C7',
            'MENTAL': '#7C3AED',
            'FISICA': '#059669',
            'SOCIAL': '#E11D48',
            'ODONTO': '#0D9488',
            'NUTRICAO': '#65A30D',
        }
        return mapa_cores.get(self.categoria, '#0284C7')