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