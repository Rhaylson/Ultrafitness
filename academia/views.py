from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.contrib.auth import logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.http import JsonResponse
from django.views import generic, View
from django.shortcuts import redirect
from .models import *
from .forms import ClienteForm, EnderecoForm
from datetime import datetime


def check_permissao(user):
    if user.is_authenticated and user.groups.filter(name="Recepcionista"):
        return True
    else:
        raise Http404("Acesso não permitido.")


def error_400(request, exception):
    data = {}
    return render(request, 'erros/400.html', data)


def error_403(request, exception):
    data = {}
    return render(request, 'erros/403.html', data)


def error_404(request, exception):
    data = {}
    return render(request, 'erros/404.html', data)


def error_500(request):
    data = {}
    return render(request, 'erros/500.html', data)


class BuscaCliente(UserPassesTestMixin, View):
    def test_func(self):
        return check_permissao(self.request.user)

    def get(self, request):
        busca = request.GET['busca']
        clientes = {}
        data = False
        result = False
        if busca and busca != '':
            if busca.isnumeric():
                result = Cliente.objects.filter(cpf__contains=busca)
            else:
                result = Cliente.objects.filter(nome__contains=busca)
            for cliente in result:
                clientes[cliente.cpf] = cliente.nome
            data = {
                'clientes': clientes
            }
        return JsonResponse(data, safe=False)


class ClientView(UserPassesTestMixin, generic.ListView):
    model = Cliente
    context_object_name = 'clientes'
    template_name = "clientes.html"

    def get_queryset(self):
        return Cliente.objects.order_by('nome')

    def test_func(self):
        return check_permissao(self.request.user)


class ClienteDetailView(UserPassesTestMixin, generic.DetailView):
    model = Cliente
    pk_url_kwarg = 'cpf'
    context_object_name = "cliente"
    template_name = "cliente_detail.html"

    def test_func(self):
        return check_permissao(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ferias'] = Ferias.objects.filter(dataInicioProgramacao__lt=datetime.now().date())
        cliente = context['cliente']
        if cliente.matricula != 0:
            pg_futuro = cliente.matricula.pagamento_futuro
            pagamentos = cliente.matricula.pagamentos_em_aberto
            if cliente.matricula.datamatricula != pg_futuro:
                if (datetime.now().date() - pg_futuro).days <= 15:
                    pagamentos.append(pg_futuro)
            context['pagamentos'] = pagamentos
            if pg_futuro != cliente.matricula.datamatricula:
                context['pg_futuro'] = pg_futuro
        return context


def index(request):
    usuario = request.user
    if usuario.is_authenticated:
        grupos_usuario = usuario.groups
        perfil = grupos_usuario.filter(name="Recepcionista")
        if perfil:
            return redirect("academia:clientes")
        else:
            logout(request)
    return redirect('login')

@user_passes_test(check_permissao)
def realizar_matricula(request):
    lista_planos = Plano.objects.all()
    if request.method == 'POST':
        cpf = request.POST['cpf']
        plano = request.POST['plano']
        nome = request.POST['nome']
        try:
            cliente = get_object_or_404(Cliente, pk=cpf)
            plano = get_object_or_404(Plano, pk=plano)
        except Http404:
            messages.error(request, "Dados da matrícula inválidos")
            context = {'planos': lista_planos}
            return render(request, 'realizar_matricula.html', context)

        if cliente.matricula == 0 and cliente.nome == nome:
            matricula = Matricula()
            matricula.cliente = cliente
            matricula.plano = plano
            matricula.datamatricula = datetime.now().date()
            matricula.save()
            messages.success(request, 'Matrícula Realizada com Sucesso')
            return redirect("academia:cliente", cpf)
        else:
            if cliente.nome != nome:
                messages.error(request, "Nome do cliente não correspondente")
                context = {'cliente': cliente, 'planos': lista_planos}
            if cliente.matricula != 0:
                messages.error(request, "O cliente já possui uma matrícula ativa")
                context = {'cliente': cliente, 'planos': lista_planos}
            return render(request, 'realizar_matricula.html', context)
    context = {'planos': lista_planos}
    return render(request, 'realizar_matricula.html', context)

@user_passes_test(check_permissao)
def registrar_pagamento(request):
    if request.method == 'POST':
        mat = request.POST['matricula']
        ref = request.POST['referencia']
        cpf = request.POST['cpf']
        cliente = get_object_or_404(Cliente, pk=cpf)
        if cliente.matricula.matricula == int(mat) and cliente.matricula.pagamento_esperado == ref:
            pg = Pagamento()
            pg.cliente = cliente
            pg.matricula = cliente.matricula
            pg.referencia = ref
            pg.valor = cliente.matricula.plano.valor
            pg.data = datetime.now().date()
            pg.save()
            messages.success(request, 'Pagamento registrado com sucesso')
            return redirect("academia:cliente", cpf=cpf)
        else:
            messages.error(request,
                           'Dados do pagamento inválidos. Verifique se não existe pagamento anterior em aberto')
            return render(request, "cliente_detail.html", {"cliente": cliente})
    else:
        return redirect("index")

@user_passes_test(check_permissao)
def registrar_ferias(request):
    if request.method == 'POST':

        # Recupera os dados do formuário quando a requisição for POST
        mat = request.POST['matricula']
        cpf = request.POST['cpf']
        ano = request.POST['ano']
        update = False
        insert = False

        # Busca os  registros no banco de dados
        cliente = get_object_or_404(Cliente, pk=cpf)
        ferias = get_object_or_404(Ferias, pk=int(ano))
        matricula = get_object_or_404(Matricula, pk=int(mat))

        # Lista onde serão salvas as parcelas de férias. Uma terá a data de início e a outra as datas de fim.
        parcelas_inicio = []
        parcelas_fim = []

        # busca a matrícula recente do cliente
        cliente_matricula = cliente.matricula

        # Se as matrículas batem e o plano é anual
        if cliente_matricula.matricula == matricula.matricula and matricula.plano.tipo == Tipo.ANUAL:
            data_atual = datetime.now().date()
            for i in range(1, 4):
                data_inicio_parcela = request.POST["di{}{}".format(ano, i)]
                data_fim_parcela = request.POST["df{}{}".format(ano, i)]

                if data_inicio_parcela.strip() != "" and data_fim_parcela.strip() != "":
                    data_inicio_parcela = datetime.strptime(data_inicio_parcela, '%d/%m/%Y').date()
                    data_fim_parcela = datetime.strptime(data_fim_parcela, '%d/%m/%Y').date()

                    if data_atual < data_inicio_parcela <= data_fim_parcela:
                        if ferias.dataInicioProgramacao <= data_inicio_parcela and data_fim_parcela <= ferias.dataFimProgramacao:
                            # Já existem datas na lista
                            if len(parcelas_inicio) > 1:
                                data_f_anterior = parcelas_fim[len(parcelas_fim) - 1] + timedelta(days=1)
                                if data_inicio_parcela > data_f_anterior:
                                    parcelas_inicio.append(data_inicio_parcela)
                                    parcelas_fim.append(data_fim_parcela)
                            else:
                                parcelas_inicio.append(data_inicio_parcela)
                                parcelas_fim.append(data_fim_parcela)

            parcelas = Parcela.objects.filter(matricula=mat).filter(ferias__anoReferencia=ano)
            qtd_parcelas = len(parcelas_inicio)

            if qtd_parcelas == 0 and parcelas.count() == 0:
                messages.error(request, "Não existem parcelas no ano de {} para serem excluídas".format(ano))

            for p, parcela in enumerate(parcelas):
                if qtd_parcelas == 0 and parcelas.count() > 0:
                    parcelas.delete()
                    messages.success(request, "Parcelas do ano {} excluídas com sucesso".format(ano))
                    break
                elif p < qtd_parcelas:
                    parcela.dataInicio = parcelas_inicio[p]
                    parcela.dataFim = parcelas_fim[p]
                    parcela.save()
                    update = True
                else:
                    parcela.delete()

            if qtd_parcelas > parcelas.count():
                if parcelas.count() == 0:
                    insert = True
                for p2 in range(parcelas.count(), qtd_parcelas):
                    nova_parcela = Parcela()
                    nova_parcela.ferias = ferias
                    nova_parcela.dataInicio = parcelas_inicio[p2]
                    nova_parcela.dataFim = parcelas_fim[p2]
                    nova_parcela.matricula = cliente_matricula
                    nova_parcela.parcela = str(p2 + 1)
                    nova_parcela.save()

            if insert:
                messages.success(request, "Férias do ano de {} salvas com sucesso".format(ano))
            elif update:
                messages.success(request, "Férias do ano de {} alterada com sucesso".format(ano))

    messages.info(request, ano, "ano")
    return redirect("academia:cliente", cpf=cpf)

@user_passes_test(check_permissao)
def adicionar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        form2 = EnderecoForm(request.POST)
        if form.is_valid() and form2.is_valid():
            endereco = form2.save()
            cliente = form.save(commit=False)
            cliente.endereco = endereco
            cliente.save()
            context = {'cliente': cliente, 'planos': Plano.objects.all()}
            messages.success(request, 'Cliente cadastrado com sucesso. Complete a matrícula')
            return render(request, "realizar_matricula.html", context)
        else:
            return render(request, 'gerenciar_cliente.html',
                          {'form_endereco': form2, 'form': form})
    form = ClienteForm()
    form2 = EnderecoForm()
    return render(request, 'gerenciar_cliente.html', {'form_endereco': form2, 'form': form})

@user_passes_test(check_permissao)
def editar_cliente(request, cpf):
    cliente = get_object_or_404(Cliente, pk=cpf)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        form2 = EnderecoForm(request.POST, instance=cliente.endereco)
        if form.is_valid() and form2.is_valid():
            endereco = form2.save()
            cliente.endereco = endereco
            cliente.save()
            messages.success(request, 'Cliente alterado com sucesso')
            return redirect("academia:clientes")
        else:
            context = {'cpf': cpf, 'form_endereco': form2, 'form': form}
            return render(request, "gerenciar_cliente.html", context)
    form = ClienteForm(instance=cliente)
    form2 = EnderecoForm(instance=cliente.endereco)
    context = {'cpf': cpf, 'form_endereco': form2, 'form': form}
    return render(request, "gerenciar_cliente.html", context)

@user_passes_test(check_permissao)
def excluir_cliente(request, cpf):
    cliente = get_object_or_404(Cliente, pk=cpf)
    if request.method == 'GET':
        matriculas = Matricula.objects.filter(cliente=cliente)
        if not matriculas:
            cliente.delete()
            messages.success(request, "Cliente {} deletado com sucesso".format(cliente.nome))
        else:
            messages.error(request, "Não é possível excluir um cliente que já tenha se matriculado")
    else:
        messages.error(request, "Solicitação inválida")
    return redirect("academia:clientes")

@user_passes_test(check_permissao)
def busca_por_nome(request):
    if request.method == 'GET':
        return redirect("academia:clientes")
    elif request.method == 'POST':
        busca = request.POST['busca']
        tipo = request.POST['tipo']
        clientes = []
        if tipo:
            if busca == '':
                resultado = Cliente.objects.all().order_by('nome')
            else:
                resultado = Cliente.objects.filter(nome__icontains=busca).order_by('nome')
            if resultado.first() and tipo != "todos":
                for cliente in resultado:
                    if tipo == "ativo":
                        if cliente.matricula != 0:
                            clientes.append(cliente)
                    elif tipo == "inativo":
                        if cliente.matricula == 0:
                            clientes.append(cliente)
            else:
                return render(request, 'clientes.html', {'clientes': resultado})
    else:
        return redirect("academia:clientes")
    return render(request, 'clientes.html', {'clientes': clientes})
