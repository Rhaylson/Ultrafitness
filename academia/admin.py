from django.contrib import admin
from academia.models import Pessoa_Fisica, Fisioterapeuta, Cliente, Avaliacao, Plano, Instrutor, Aula, Ferias, \
    Matricula, Parcela, Pagamento, RegistroAula, Frequencia, RegistroDiaAula, Endereco

admin.site.register(Cliente)
admin.site.register(Instrutor)
admin.site.register(Fisioterapeuta)
admin.site.register(Avaliacao)
admin.site.register(Plano)
admin.site.register(Aula)
admin.site.register(Ferias)
admin.site.register(Parcela)
admin.site.register(Matricula)
admin.site.register(Frequencia)
admin.site.register(Pagamento)
admin.site.register(RegistroDiaAula)
admin.site.register(RegistroAula)
admin.site.register(Endereco)

