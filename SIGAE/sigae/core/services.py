"""Regras de negócio. Toda alteração de estoque passa por transações com row-lock."""
import uuid

from django.db import transaction
from django.utils import timezone

from .models import Equipamento, Reserva

S, R = Equipamento.Status, Reserva.Status


class ReservaError(Exception):
    pass


@transaction.atomic
def criar_reservas(solicitante, data, turno, quantidade, turma=None):
    """Reserva (feita pelo instrutor para a turma) de 1 ou N notebooks.

    SELECT ... FOR UPDATE trava os notebooks escolhidos: duas requisições simultâneas
    não conseguem pegar o mesmo equipamento (evita race condition). Os notebooks já
    ficam pré-alocados como 'Reservado'; o Administrador confirma/troca na entrega.
    """
    notebooks = list(
        Equipamento.objects.select_for_update().filter(status=S.DISPONIVEL).order_by("numero")[:quantidade]
    )
    if len(notebooks) < quantidade:
        raise ReservaError(f"Só há {len(notebooks)} notebook(s) disponível(is); você pediu {quantidade}.")

    Equipamento.objects.filter(pk__in=[n.pk for n in notebooks]).update(status=S.RESERVADO)
    lote = uuid.uuid4() if quantidade > 1 else None
    return Reserva.objects.bulk_create([
        Reserva(solicitante=solicitante, turma=turma, equipamento=n, data=data, turno=turno,
                quantidade=quantidade, lote=lote, status=R.PENDENTE)
        for n in notebooks
    ])


@transaction.atomic
def entregar(reserva_id, numero, admin):
    reserva = Reserva.objects.select_for_update().select_related("equipamento").get(pk=reserva_id)
    if not reserva.aguardando_entrega:
        raise ReservaError("Esta reserva não está aguardando entrega.")
    try:
        novo = Equipamento.objects.select_for_update().get(numero=numero)
    except Equipamento.DoesNotExist:
        raise ReservaError(f"Notebook {numero} não existe.")

    atual = reserva.equipamento
    if atual is None or atual.pk != novo.pk:
        if novo.status != S.DISPONIVEL:
            raise ReservaError(f"{novo} não está disponível ({novo.get_status_display()}).")
        if atual:  # libera o notebook pré-alocado que foi trocado
            Equipamento.objects.filter(pk=atual.pk).update(status=S.DISPONIVEL)

    novo.status = S.EMPRESTADO
    novo.save(update_fields=["status"])
    reserva.equipamento, reserva.status = novo, R.ATIVA
    reserva.entregue_em, reserva.entregue_por = timezone.now(), admin
    reserva.save()
    return reserva


@transaction.atomic
def devolver(reserva_id):
    reserva = Reserva.objects.select_for_update().select_related("equipamento").get(pk=reserva_id)
    if not reserva.esta_ativa:
        raise ReservaError("Esta reserva não está com equipamento entregue.")
    Equipamento.objects.filter(pk=reserva.equipamento_id).update(status=S.DISPONIVEL)
    reserva.status, reserva.devolvida_em = R.CONCLUIDA, timezone.now()
    reserva.save(update_fields=["status", "devolvida_em"])
    return reserva


@transaction.atomic
def cancelar(reserva_id, usuario):
    reserva = Reserva.objects.select_for_update().get(pk=reserva_id)
    if not (usuario.is_administrador or reserva.solicitante_id == usuario.pk):
        raise ReservaError("Você não pode cancelar esta reserva.")
    if not reserva.aguardando_entrega:
        raise ReservaError("Só é possível cancelar reservas aguardando entrega.")
    if reserva.equipamento_id:
        Equipamento.objects.filter(pk=reserva.equipamento_id).update(status=S.DISPONIVEL)
    reserva.status = R.CANCELADA
    reserva.save(update_fields=["status"])
    return reserva


@transaction.atomic
def resgatar(aluno, data):
    """O aluno 'recolhe' um dos notebooks que o instrutor reservou para a turma dele."""
    from .models import User
    aluno = User.objects.select_for_update().get(pk=aluno.pk)  # serializa cliques repetidos do mesmo aluno
    if not aluno.turma_id:
        raise ReservaError("Você não está vinculado a nenhuma turma.")
    if Reserva.objects.filter(aluno=aluno, data=data, status__in=[R.PENDENTE, R.APROVADA, R.ATIVA]).exists():
        raise ReservaError("Você já resgatou um notebook para hoje.")
    livre = (Reserva.objects.select_for_update()
             .filter(turma_id=aluno.turma_id, data=data, aluno__isnull=True, status__in=[R.PENDENTE, R.APROVADA])
             .order_by("equipamento__numero").first())
    if livre is None:
        raise ReservaError("Não há notebook reservado disponível para a sua turma hoje.")
    livre.aluno = aluno
    livre.save(update_fields=["aluno"])
    return livre
