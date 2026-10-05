import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Turno(models.TextChoices):
    MATUTINO = "MAT", "Matutino"
    VESPERTINO = "VES", "Vespertino"
    NOTURNO = "NOT", "Noturno"


class Turma(models.Model):
    nome = models.CharField("Nome da turma", max_length=100)
    turno = models.CharField(max_length=3, choices=Turno.choices)
    instrutor = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
        related_name="turmas_lecionadas", verbose_name="Instrutor responsável",
    )

    class Meta:
        ordering = ["turno", "nome"]

    def __str__(self):
        return f"{self.nome} ({self.get_turno_display()})"


class User(AbstractUser):
    """Perfis (Aluno / Instrutor / Administrador) são Groups do Django."""
    email = models.EmailField("E-mail educacional", unique=True)
    turma = models.ForeignKey(Turma, null=True, blank=True, on_delete=models.SET_NULL, related_name="alunos")
    turno = models.CharField(max_length=3, choices=Turno.choices, blank=True)

    GRUPO_ALUNO, GRUPO_INSTRUTOR, GRUPO_ADMIN = "Aluno", "Instrutor", "Administrador"

    def _tem_grupo(self, nome):
        return self.groups.filter(name=nome).exists()

    @property
    def nome_completo(self):
        return self.get_full_name() or self.username

    @property
    def is_aluno(self):
        return self._tem_grupo(self.GRUPO_ALUNO)

    @property
    def is_instrutor(self):
        return self._tem_grupo(self.GRUPO_INSTRUTOR)

    @property
    def is_administrador(self):
        return self.is_superuser or self._tem_grupo(self.GRUPO_ADMIN)

    @property
    def perfil(self):
        if self.is_administrador:
            return "Administrador"
        return "Instrutor" if self.is_instrutor else "Aluno"


class Equipamento(models.Model):
    class Status(models.TextChoices):
        DISPONIVEL = "DIS", "Disponível"
        RESERVADO = "RES", "Reservado"
        EMPRESTADO = "EMP", "Emprestado"
        MANUTENCAO = "MAN", "Manutenção"

    numero = models.PositiveSmallIntegerField(
        "Número", unique=True, validators=[MinValueValidator(1), MaxValueValidator(45)],
    )
    status = models.CharField(max_length=3, choices=Status.choices, default=Status.DISPONIVEL, db_index=True)

    class Meta:
        ordering = ["numero"]
        verbose_name = "Equipamento (Notebook)"
        verbose_name_plural = "Equipamentos (Notebooks)"

    def __str__(self):
        return f"Notebook {self.numero:02d}"

    @property
    def badge_class(self):
        return {"DIS": "bg-success", "RES": "bg-warning text-dark",
                "EMP": "bg-primary", "MAN": "bg-secondary"}[self.status]


class Reserva(models.Model):
    class Status(models.TextChoices):
        PENDENTE = "PEN", "Pendente"
        APROVADA = "APR", "Reservada"
        ATIVA = "ATI", "Entregue"
        CONCLUIDA = "CON", "Concluída"
        CANCELADA = "CAN", "Cancelada"

    solicitante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="reservas",
                                    verbose_name="Instrutor (quem reservou)")
    turma = models.ForeignKey(Turma, null=True, blank=True, on_delete=models.SET_NULL, related_name="reservas")
    aluno = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
                              related_name="notebooks_resgatados", verbose_name="Aluno que resgatou")
    equipamento = models.ForeignKey(Equipamento, null=True, blank=True, on_delete=models.PROTECT, related_name="reservas")
    data = models.DateField("Data da reserva", db_index=True)
    turno = models.CharField("Turno da reserva", max_length=3, choices=Turno.choices)
    quantidade = models.PositiveSmallIntegerField("Quantidade solicitada (total do lote)", default=1)
    lote = models.UUIDField(null=True, blank=True, db_index=True)
    status = models.CharField(max_length=3, choices=Status.choices, default=Status.PENDENTE, db_index=True)
    criada_em = models.DateTimeField(auto_now_add=True)
    entregue_em = models.DateTimeField("Data/hora de entrega", null=True, blank=True)
    devolvida_em = models.DateTimeField("Data/hora de devolução", null=True, blank=True)
    entregue_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="entregas_realizadas",
    )

    class Meta:
        ordering = ["-data", "turno", "-criada_em"]

    def __str__(self):
        return f"Reserva #{self.pk} - {self.solicitante} - {self.data:%d/%m/%Y} {self.get_turno_display()}"

    @property
    def aguardando_entrega(self):
        return self.status in (self.Status.PENDENTE, self.Status.APROVADA)

    @property
    def esta_ativa(self):
        return self.status == self.Status.ATIVA

    @property
    def badge_class(self):
        return {"PEN": "bg-warning text-dark", "APR": "bg-info text-dark", "ATI": "bg-primary",
                "CON": "bg-success", "CAN": "bg-secondary"}[self.status]

    @property
    def head_class(self):
        return {"PEN": "head-proximo", "APR": "head-proximo", "ATI": "head-atual",
                "CON": "head-encerrado", "CAN": "head-encerrado"}[self.status]

    @property
    def solicitado_por(self):
        return self.aluno or self.solicitante

    @property
    def data_hora(self):
        return self.entregue_em or self.criada_em
