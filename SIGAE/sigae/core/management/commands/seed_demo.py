from django.core.management.base import BaseCommand
from django.utils import timezone

from core import services
from core.models import Equipamento, Reserva, Turma, Turno, User

ABERTAS = [Reserva.Status.PENDENTE, Reserva.Status.APROVADA, Reserva.Status.ATIVA]


class Command(BaseCommand):
    help = "Cria reservas de exemplo para HOJE. Use --reset para apagar as de hoje e recriar."

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true", help="Apaga as reservas abertas de hoje e recria o demo")

    def handle(self, *args, **opts):
        hoje = timezone.localdate()
        antigas = Reserva.objects.filter(data=hoje, status__in=ABERTAS)
        if not opts["reset"]:
            antigas = antigas.filter(turma__isnull=True)  # só resíduos da versão antiga do demo
        ids = list(antigas.values_list("equipamento_id", flat=True))
        antigas.delete()
        Equipamento.objects.filter(pk__in=ids).exclude(status=Equipamento.Status.MANUTENCAO).update(
            status=Equipamento.Status.DISPONIVEL)

        if Reserva.objects.filter(data=hoje).exists():
            self.stdout.write("Já existem reservas para hoje; use --reset para recriar.")
            return

        for username, turno, qtd in [
            ("instrutor.a", Turno.MATUTINO, 8),
            ("instrutor.a", Turno.VESPERTINO, 5),
            ("instrutor.b", Turno.NOTURNO, 6),
        ]:
            inst = User.objects.get(username=username)
            turma = Turma.objects.get(instrutor=inst, turno=turno)
            services.criar_reservas(inst, hoje, turno, qtd, turma)

        admin = User.objects.get(username="admin.sigae")
        r = services.resgatar(User.objects.get(username="aluno01"), hoje)     # aluno01 solicitou...
        services.entregar(r.pk, r.equipamento.numero, admin)                  # ...e já retirou (aparece em Ativos)
        services.resgatar(User.objects.get(username="aluno06"), hoje)         # aluno06 solicitou (aparece em Solicitações)
        self.stdout.write(self.style.SUCCESS("Demo criado: aluno01 com notebook entregue, aluno06 aguardando entrega."))
