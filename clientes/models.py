from django.db import models


class Cliente(models.Model):

    STATUS = (
        ("ATIVO", "Ativo"),
        ("INATIVO", "Inativo"),
    )

    SEXO = (
        ("M", "Masculino"),
        ("F", "Feminino"),
        ("O", "Outro"),
    )

    nome = models.CharField("Nome", max_length=150)

    cpf = models.CharField(
        "CPF",
        max_length=14,
        blank=True,
        null=True
    )

    nascimento = models.DateField(
        "Nascimento",
        blank=True,
        null=True
    )

    sexo = models.CharField(
        "Sexo",
        max_length=1,
        choices=SEXO,
        blank=True
    )

    telefone = models.CharField(
        "Telefone",
        max_length=20,
        blank=True
    )

    whatsapp = models.CharField(
        "WhatsApp",
        max_length=20,
        blank=True
    )

    email = models.EmailField(
        "E-mail",
        blank=True
    )

    cep = models.CharField(
        max_length=9,
        blank=True
    )

    endereco = models.CharField(
        max_length=200,
        blank=True
    )

    numero = models.CharField(
        max_length=10,
        blank=True
    )

    bairro = models.CharField(
        max_length=100,
        blank=True
    )

    cidade = models.CharField(
        max_length=100,
        blank=True
    )

    uf = models.CharField(
        max_length=2,
        blank=True
    )

    profissional = models.ForeignKey(
        "usuarios.Usuario",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clientes"
    )

    valor_sessao = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    total_sessoes = models.PositiveIntegerField(
        default=10
    )

    sessoes_realizadas = models.IntegerField(
    default=0
)

    status = models.CharField(
        max_length=10,
        choices=STATUS,
        default="ATIVO"
    )

    observacoes = models.TextField(
        blank=True
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    atualizado_em = models.DateTimeField(
        auto_now=True
    )

    @property
    def sessoes_restantes(self):

        return max(
            0,
            self.total_sessoes -
            self.sessoes_realizadas
        )

    def __str__(self):

        return self.nome

    class Meta:

        ordering = ["nome"]

        verbose_name = "Cliente"

        verbose_name_plural = "Clientes"