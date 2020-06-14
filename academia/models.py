from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta, date
from dateutil import relativedelta
from validate_docbr import CPF


class Pessoa_Fisica(models.Model):
    cpf = models.CharField(max_length=11, primary_key=True)
    identidade = models.CharField(max_length=45, unique=True)
    nome = models.CharField(max_length=150)
    dataNascimento = models.DateField()
    endereco = models.OneToOneField('Endereco', on_delete=models.CASCADE)
    telefone = models.CharField(max_length=25, default='')

    @property
    def get_dataNascimento(self):
        return self.dataNascimento.strftime("%d/%m/%Y")

    def clean(self):
        cpf = CPF()
        super().clean()
        dic_erros = {}
        if self.dataNascimento >= datetime.now().date():
            dic_erros['dataNascimento'] = ValidationError('Data de Nascimento inválida')
        if not cpf.validate(self.cpf):
            dic_erros['cpf'] = ValidationError('Número de CPF inválido')
        if dic_erros:
            raise ValidationError(dic_erros)

    class Meta:
        db_table = "pessoa_fisica"
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'


class Fisioterapeuta(Pessoa_Fisica):
    registroConselho = models.CharField(max_length=45, primary_key=True)
    avaliacoes = models.ManyToManyField('Cliente', through="Avaliacao", related_name="avaliacoes")

    class Meta:
        db_table = "fisioterapeuta"
        verbose_name = 'Fisioterapeuta'
        verbose_name_plural = 'Fisioterapeutas'


class Cliente(Pessoa_Fisica):
    impressaodigital = models.TextField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parcelas_ferias = {}
        self._get_ferias()

    def __str__(self):
        return "{} - {}".format(self.cpf, self.nome)

    def _get_ferias(self):
        data_atual = datetime.now().date()
        mat = self.matricula
        if mat != 0:
            if mat.plano.tipo == Tipo.ANUAL:
                ferias = Ferias.objects.filter(anoReferencia__range=[mat.datamatricula.year, data_atual.year])
                for f in ferias:
                    parcelas = mat.parcela_set.filter(ferias__anoReferencia=f.anoReferencia)
                    self._adiciona_parcelas(parcelas, f.anoReferencia)
                ano_seguinte = Ferias.objects.filter(anoReferencia=(data_atual.year + 1)).first()
                if ano_seguinte:
                    if data_atual >= ano_seguinte.dataInicioProgramacao:
                        parcelas = mat.parcela_set.filter(ferias__anoReferencia=ano_seguinte.anoReferencia)
                        self._adiciona_parcelas(parcelas, ano_seguinte.anoReferencia)
            else:
                return False
        else:
            return False

    def _adiciona_parcelas(self, parcelas, ano):
        self.parcelas_ferias[ano] = {}
        for i in range(1, 4):
            parcela = parcelas.filter(parcela=i).first()
            if parcela:
                dias = parcela.dataFim - parcela.dataInicio
                self.parcelas_ferias[ano][parcela.parcela] = {"p": parcela.parcela, "inicio": parcela.dataInicio,
                                                              "fim": parcela.dataFim, "dias": dias.days + 1}
            else:
                self.parcelas_ferias[ano][i] = {"p": i, "inicio": "", "fim": "", "status": ""}

    @property
    def matricula(self):
        matricula = self.matricula_set.last()
        if matricula:
            return matricula
        return 0

    @property
    def pagamentos(self):
        if self.matricula != 0:
            return self.matricula.pagamentos_efetuados
        return {}

    class Meta:
        db_table = "cliente"
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'


class Avaliacao(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fisioterapeuta = models.ForeignKey(Fisioterapeuta, on_delete=models.CASCADE)
    data = models.DateField()
    ergometria = models.TextField()
    dobrascutaneas = models.TextField()
    anamnese = models.TextField()

    class Meta:
        db_table = "avaliacao"
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'


class Modalidade(models.TextChoices):
    GRUPO = 'GRP', "Grupo"
    MUSCULACAO = "MUSC", "Musculação"


class Estado(models.TextChoices):
    AC = 'AC', 'Acre'
    AL = 'AL', 'Alagoas'
    AP = 'AP', 'Amapá'
    AM = 'AM', 'Amazonas'
    BA = 'BA', 'Bahia'
    CE = 'CE', 'Ceará'
    DF = 'DF', 'Distrito Federal'
    ES = 'ES', 'Espírito Santo'
    GO = 'GO', 'Goiás'
    MA = 'MA', 'Maranhão'
    MT = 'MT', 'Mato Grosso'
    MS = 'MS', 'Mato Grosso do Sul'
    MG = 'MG', 'Minas Gerais'
    PA = 'PA', 'Pará'
    PB = 'PB', 'Paraíba'
    PR = 'PR', 'Paraná'
    PE = 'PE', 'Pernambuco'
    PI = 'PI', 'Piauí'
    RJ = 'RJ', 'Rio de Janeiro'
    RN = 'RN', 'Rio Grande do Norte'
    RS = 'RS', 'Rio Grande do Sul'
    RO = 'RO', 'Rondônia'
    RR = 'RR', 'Roraima'
    SC = 'SC', 'Santa Catarina'
    SP = 'SP', 'São Paulo'
    SE = 'SE', 'Sergipe'
    TO = 'TO', 'Tocantins'


class Endereco(models.Model):
    complemento = models.CharField(max_length=120)
    cidade = models.CharField(max_length=45)
    bairro = models.CharField(max_length=45)
    estado = models.CharField(max_length=2, choices=Estado.choices)

    def __str__(self):
        return "{}, {}, {}, {}".format(self.complemento, self.bairro, self.cidade, self.estado)

    class Meta:
        db_table = 'endereco'
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"


class Dia_Semana(models.TextChoices):
    SEGUNDA = "1", "Segunda-Feira"
    TERÇA = "2", "Terça-Feira"
    QUARTA = "3", "Quarta-Feira"
    QUINTA = "4", "Quinta-Feira"
    SEXTA = "5", "Sexta-Feira"
    SÁBADO = "6", "Sábado"
    DOMINGO = "7", "Domingo"


class Tipo(models.TextChoices):
    MENSAL = "M", "MENSAL"
    ANUAL = "A", "ANUAL"


class Plano(models.Model):
    valor = models.FloatField()
    tipo = models.CharField(max_length=10, choices=Tipo.choices, primary_key=True)
    matriculas = models.ManyToManyField(Cliente, through='Matricula', related_name="matriculas")

    @property
    def tipoplano(self):
        for tupla in Tipo.choices:
            if self.tipo == tupla[0]:
                return tupla[1]

    class Meta:
        db_table = "plano"
        verbose_name = 'Plano'
        verbose_name_plural = 'Planos'

    def __str__(self):
        return "{} - {}".format(self.valor, self.tipoplano)


class Instrutor(Pessoa_Fisica):
    modalidade = models.CharField(max_length=4, choices=Modalidade.choices, default=Modalidade.MUSCULACAO)

    class Meta:
        db_table = "instrutor"
        verbose_name = 'Instrutor'
        verbose_name_plural = 'Instrutores'


class Aula(models.Model):
    turma = models.CharField(max_length=45, primary_key=True)
    nome = models.CharField(max_length=45)
    horaInicio = models.TimeField()
    horaFim = models.TimeField()
    sala = models.CharField(max_length=45)
    instrutor = models.ForeignKey(Instrutor, on_delete=models.CASCADE)

    class Meta:
        db_table = "aula"
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'


class Ferias(models.Model):
    anoReferencia = models.IntegerField(primary_key=True)
    dataInicioProgramacao = models.DateField()
    dataFimProgramacao = models.DateField()

    class Meta:
        db_table = "ferias"
        verbose_name = 'Férias'
        verbose_name_plural = 'Férias'

    def clean(self):
        super().clean()
        if self.dataInicioProgramacao != date(self.anoReferencia, 1, 1) \
                or self.dataFimProgramacao != date(self.anoReferencia, 12, 31):

            raise ValidationError("Período Inválido")


class Matricula(models.Model):
    matricula = models.AutoField(primary_key=True)
    situacao = models.BooleanField(default=1)
    datamatricula = models.DateField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    ferias = models.ManyToManyField(Ferias, through='Parcela', related_name="ferias")
    plano = models.ForeignKey(Plano, on_delete=models.CASCADE)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pagamentos_em_aberto = self.get_pagamentos_em_aberto()

    def __str__(self):
        return str(self.matricula)

    def _get_dias_ferias(self, ano=datetime.now().date().year):
        consulta = self.parcela_set.filter(ferias__anoReferencia=ano)
        dias = 0
        if consulta.count() > 0:
            for parcela in consulta:
                if parcela.dataFim == parcela.dataInicio:
                    dias = dias + 1
                else:
                    dias = dias + (parcela.dataFim - parcela.dataInicio).days + 1
        return dias

    @property
    def get_dataMatricula(self):
        return self.datamatricula.strftime("%d/%m/%Y")

    @property
    def pagamento_futuro(self):
        proximo_pagamento = self.datamatricula
        em_aberto = self.pagamentos_em_aberto

        dias = 0
        if len(em_aberto) == 0:
            ultimo_pagamento = self.pagamento_set.last()
            if self.plano.tipo == Tipo.ANUAL:
                anos = int(ultimo_pagamento.referencia) - self.datamatricula.year
                if anos > 0:
                    for i in range(0, anos):
                        dias += self._get_dias_ferias(ano=self.datamatricula.year + i)
                dias += self._get_dias_ferias()
                proximo_pagamento = self.datamatricula + relativedelta.relativedelta(years=+(anos+1), days=+dias)
            elif self.plano.tipo == Tipo.MENSAL:
                mes = ultimo_pagamento.referencia.split('/')[0]
                ano = ultimo_pagamento.referencia.split('/')[1]
                proximo_pagamento = self._retorna_vencimento(self.datamatricula.day, mes, ano) + relativedelta.relativedelta(months=+1)
        return proximo_pagamento

    def _retorna_vencimento (self, dia, mes, ano):
        try:
            data = datetime(int(ano), int(mes), int(dia))
        except ValueError:
            if mes == 2 and dia > 28:
                data = datetime(ano, mes+1, 1)
            elif dia > 30:
                data = datetime(ano, mes+1, 1)
            else:
                data = datetime(ano, mes, 30)
        return data

    def get_pagamentos_em_aberto(self):
        pagamentos = []
        ultimo_pagamento = self.pagamento_set.last()
        if ultimo_pagamento:
            dia_base = self.datamatricula.day
            data_atual = datetime.now()
            referencia_lista = ultimo_pagamento.referencia.split('/')
            if len(referencia_lista) == 2:
                mes = int(referencia_lista[0])
                ano = int(referencia_lista[1])
            else:
                mes = self.datamatricula.month
                ano = int(ultimo_pagamento.referencia)

            referencia = self._retorna_vencimento(dia_base, mes, ano)
            if self.plano.tipo == Tipo.MENSAL:
                dif_meses = (data_atual - referencia).days / 30
                meses = int(dif_meses)
                for i in range(1, (meses + 1)):
                    pagamentos.append((referencia + relativedelta.relativedelta(months=+i)).date())

            elif self.plano.tipo == Tipo.ANUAL:
                dias_ferias = self._get_dias_ferias()
                referencia = referencia + relativedelta.relativedelta(days=+dias_ferias)
                dif_meses = relativedelta.relativedelta(data_atual, referencia)
                for i in range(1, dif_meses.years):
                    pagamentos.append((referencia + relativedelta.relativedelta(year=+i)).date())
        else:
            pagamentos.append(self.datamatricula)
        return pagamentos

    @property
    def pagamentos_efetuados(self):
        return self.pagamento_set.all().order_by('referencia')

    @property
    def pagamento_esperado(self):
        retorno = ""
        ultimo_pagamento = self.pagamento_set.last()
        if self.plano.tipo == Tipo.ANUAL and ultimo_pagamento:
            retorno = str(int(ultimo_pagamento.referencia) + 1)
        elif self.plano.tipo == Tipo.ANUAL and not ultimo_pagamento:
            retorno = "{}".format(self.datamatricula.year)
        elif self.plano.tipo == Tipo.MENSAL and ultimo_pagamento:
            ano = int(ultimo_pagamento.referencia.split('/')[1])
            mes = int(ultimo_pagamento.referencia.split('/')[0])
            if mes == 12:
                retorno = "{}/{}".format(1, ano + 1)
            else:
                if mes < 9:
                    retorno = "0{}/{}".format(mes + 1, ano)
                else:
                    retorno = "{}/{}".format(mes + 1, ano)
        else:
            if self.datamatricula.month < 9:
                retorno = "0{}/{}".format(self.datamatricula.month, self.datamatricula.year)
            else:
                retorno = "{}/{}".format(self.datamatricula.mont, self.datamatricula.year)

        return retorno

    def _status_matricula(self):
        if len(self.pagamentos_em_aberto) > 0:
            if self.pagamentos_em_aberto[0] == self.datamatricula:
                status = "inativa"
            else:
                status = "atrasada"
        else:
            status = "ativa"
        return status

    @property
    def status(self):
        status = ""
        if self.situacao == 0:
            status = "cancelada"
        else:
            status = self._status_matricula()
        return status

    class Meta:
        db_table = "matricula"
        verbose_name = 'Matrícula'
        verbose_name_plural = 'Matrículas'


class Parcela(models.Model):
    parcela = models.CharField(max_length=15)
    matricula = models.ForeignKey(Matricula, on_delete=models.CASCADE)
    ferias = models.ForeignKey(Ferias, on_delete=models.CASCADE, default=None)
    dataInicio = models.DateField()
    dataFim = models.DateField()

    class Meta:
        db_table = "parcela_ferias"
        verbose_name = 'Parcelas_Férias'
        verbose_name_plural = 'Parcelas_Férias'


class Pagamento(models.Model):
    matricula = models.ForeignKey(Matricula, on_delete=models.CASCADE)
    referencia = models.CharField(max_length=7, default=("{}-{}".format(datetime.now().month, datetime.now().year)))
    data = models.DateField()
    valor = models.FloatField()

    class Meta:
        db_table = "pagamento"
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'


class RegistroDiaAula(models.Model):
    turma = models.ForeignKey(Aula, on_delete=models.CASCADE)
    dia = models.CharField(max_length=1, choices=Dia_Semana.choices)

    class Meta:
        db_table = "dia_aula_semana"
        verbose_name = 'Registro_dias_Aulas_na_Semana'
        verbose_name_plural = 'Registro_dias_Aulas_na_Semana'


class RegistroAula(models.Model):
    turma = models.ForeignKey(Aula, on_delete=models.CASCADE)
    dia = models.DateField()

    class Meta:
        db_table = "registro_aula"
        verbose_name = 'Confirmação_de_Aula'
        verbose_name_plural = 'Confirmação_de_Aula'


class Frequencia(models.Model):
    matricula = models.ForeignKey(Matricula, models.CASCADE)
    turma = models.ForeignKey(Aula, models.CASCADE)
    entrada = models.DateTimeField()

    class Meta:
        db_table = "frequencia_aluno"
        verbose_name = 'Frequência_Cliente'
        verbose_name_plural = 'Frequência_Cliente'
