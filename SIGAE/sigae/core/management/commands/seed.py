import os

from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import Equipamento, Turma, Turno, User

NOMES = ["Ana Souza", "Bruno Lima", "Carla Dias", "Diego Rocha", "Elisa Matos",
         "Felipe Nunes", "Gabriela Reis", "Hugo Pires", "Isabela Cruz", "João Melo",
         "Karen Alves", "Lucas Prado", "Marina Costa", "Nicolas Faria", "Olívia Brito"]


class Command(BaseCommand):
    help = "Popula grupos, turmas, usuários fictícios e notebooks 1-45."

    @transaction.atomic
    def handle(self, *args, **opts):
        senha = os.getenv("SEED_PASSWORD", "sigae@2026")
        grupos = {n: Group.objects.get_or_create(name=n)[0] for n in ("Aluno", "Instrutor", "Administrador")}

        def usuario(username, nome, grupo, turno="", turma=None, staff=False):
            first, last = nome.split(" ", 1)
            u, novo = User.objects.get_or_create(username=username, defaults={
                "first_name": first, "last_name": last, "email": f"{username}@edu.sigae.local",
                "turno": turno, "turma": turma, "is_staff": staff})
            if novo:
                u.set_password(senha)
                u.save()
            u.groups.add(grupos[grupo])
            return u

        usuario("admin.sigae", "Administrador SIGAE", "Administrador", staff=True)
        inst_a = usuario("instrutor.a", "Instrutor A", "Instrutor", Turno.MATUTINO)
        inst_b = usuario("instrutor.b", "Instrutor B", "Instrutor", Turno.NOTURNO)

        turmas = [
            ("Turma A", Turno.MATUTINO, inst_a),
            ("Turma B", Turno.VESPERTINO, inst_a),
            ("Turma C", Turno.NOTURNO, inst_b),
        ]
        i = 0
        for nome, turno, instrutor in turmas:
            turma, _ = Turma.objects.get_or_create(nome=nome, turno=turno, defaults={"instrutor": instrutor})
            for _ in range(5):
                i += 1
                usuario(f"aluno{i:02d}", NOMES[i - 1], "Aluno", turno, turma)

        for n in range(1, 46):
            Equipamento.objects.get_or_create(numero=n, defaults={"status": Equipamento.Status.DISPONIVEL})

        self.stdout.write(self.style.SUCCESS(
            f"Seed concluído. Senha padrão dos usuários: {senha} (admin.sigae, instrutor.a, instrutor.b, aluno01...)"))
