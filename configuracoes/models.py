from django.db import models


class Configuracao(models.Model):

    nome_empresa = models.CharField(max_length=150)

    nome_fantasia = models.CharField(max_length=150, blank=True)

    cnpj = models.CharField(max_length=18, blank=True)

    telefone = models.CharField(max_length=20, blank=True)

    whatsapp = models.CharField(max_length=20, blank=True)

    email = models.EmailField(blank=True)

    site = models.CharField(max_length=150, blank=True)

    endereco = models.CharField(max_length=200, blank=True)

    numero = models.CharField(max_length=10, blank=True)

    bairro = models.CharField(max_length=80, blank=True)

    cidade = models.CharField(max_length=80, blank=True)

    uf = models.CharField(max_length=2, blank=True)

    cep = models.CharField(max_length=10, blank=True)

    logo = models.ImageField(
        upload_to="logos/",
        blank=True,
        null=True
    )

    recibo_prefixo = models.CharField(
        max_length=10,
        default="REC"
    )

    intervalo_agenda = models.IntegerField(
        default=30
    )

    inicio_expediente = models.TimeField()

    fim_expediente = models.TimeField()

    smtp_servidor = models.CharField(
        max_length=100,
        blank=True
    )

    smtp_porta = models.IntegerField(
        default=587
    )

    smtp_email = models.EmailField(
        blank=True
    )

    smtp_senha = models.CharField(
        max_length=100,
        blank=True
    )

    ssl = models.BooleanField(default=True)

    token_whatsapp = models.CharField(
        max_length=250,
        blank=True
    )

    ativo = models.BooleanField(default=True)

    def __str__(self):

        return self.nome_empresa