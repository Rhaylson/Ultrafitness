from datetime import date

from django.core.management import BaseCommand, CommandError
from django.contrib.auth.models import User, Group
from academia.models import Ferias, Plano, Tipo

class Command(BaseCommand):
    help = "Prepara a aplicação para uso"

    def handle(self, *args, **options):

            Group.objects.get_or_create(name="Recepcionista")
            User.objects.get_or_create(username="recepcionista")

            usuario = User.objects.get(username="recepcionista")
            usuario.set_password("123")
            usuario.groups.add(Group.objects.filter(name="Recepcionista").first())
            usuario.save()

            print("Usuário recepcionista - recepcao@123")

            p1 = Plano.objects.get_or_create(tipo=Tipo.ANUAL, valor=500)
            p2 = Plano.objects.get_or_create(tipo=Tipo.MENSAL, valor=50)


            print("Planos atualizados.")

            ferias = Ferias.objects.get_or_create(anoReferencia=2020, dataInicioProgramacao=date(2020, 1, 1),
                                                  dataFimProgramacao=date(2020, 12, 31))

            print("Ano de referência para Férias atualizado.")

