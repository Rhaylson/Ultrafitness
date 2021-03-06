# Generated by Django 3.0.5 on 2020-06-14 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aula',
            fields=[
                ('turma', models.CharField(max_length=45, primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=45)),
                ('horaInicio', models.TimeField()),
                ('horaFim', models.TimeField()),
                ('sala', models.CharField(max_length=45)),
            ],
            options={
                'verbose_name': 'Aula',
                'verbose_name_plural': 'Aulas',
                'db_table': 'aula',
            },
        ),
        migrations.CreateModel(
            name='Avaliacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('ergometria', models.TextField()),
                ('dobrascutaneas', models.TextField()),
                ('anamnese', models.TextField()),
            ],
            options={
                'verbose_name': 'Avaliação',
                'verbose_name_plural': 'Avaliações',
                'db_table': 'avaliacao',
            },
        ),
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complemento', models.CharField(max_length=120)),
                ('cidade', models.CharField(max_length=45)),
                ('bairro', models.CharField(max_length=45)),
                ('estado', models.CharField(choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')], max_length=2)),
            ],
            options={
                'verbose_name': 'Endereço',
                'verbose_name_plural': 'Endereços',
                'db_table': 'endereco',
            },
        ),
        migrations.CreateModel(
            name='Ferias',
            fields=[
                ('anoReferencia', models.IntegerField(primary_key=True, serialize=False)),
                ('dataInicioProgramacao', models.DateField()),
                ('dataFimProgramacao', models.DateField()),
            ],
            options={
                'verbose_name': 'Férias',
                'verbose_name_plural': 'Férias',
                'db_table': 'ferias',
            },
        ),
        migrations.CreateModel(
            name='Matricula',
            fields=[
                ('matricula', models.AutoField(primary_key=True, serialize=False)),
                ('situacao', models.BooleanField(default=1)),
                ('datamatricula', models.DateField()),
            ],
            options={
                'verbose_name': 'Matrícula',
                'verbose_name_plural': 'Matrículas',
                'db_table': 'matricula',
            },
        ),
        migrations.CreateModel(
            name='Pessoa_Fisica',
            fields=[
                ('cpf', models.CharField(max_length=11, primary_key=True, serialize=False)),
                ('identidade', models.CharField(max_length=45, unique=True)),
                ('nome', models.CharField(max_length=150)),
                ('dataNascimento', models.DateField()),
                ('telefone', models.CharField(default='', max_length=25)),
                ('endereco', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='academia.Endereco')),
            ],
            options={
                'verbose_name': 'Pessoa',
                'verbose_name_plural': 'Pessoas',
                'db_table': 'pessoa_fisica',
            },
        ),
        migrations.CreateModel(
            name='Plano',
            fields=[
                ('valor', models.FloatField()),
                ('tipo', models.CharField(choices=[('M', 'MENSAL'), ('A', 'ANUAL')], max_length=10, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Plano',
                'verbose_name_plural': 'Planos',
                'db_table': 'plano',
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('pessoa_fisica_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='academia.Pessoa_Fisica')),
                ('impressaodigital', models.TextField()),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'db_table': 'cliente',
            },
            bases=('academia.pessoa_fisica',),
        ),
        migrations.CreateModel(
            name='Instrutor',
            fields=[
                ('pessoa_fisica_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='academia.Pessoa_Fisica')),
                ('modalidade', models.CharField(choices=[('GRP', 'Grupo'), ('MUSC', 'Musculação')], default='MUSC', max_length=4)),
            ],
            options={
                'verbose_name': 'Instrutor',
                'verbose_name_plural': 'Instrutores',
                'db_table': 'instrutor',
            },
            bases=('academia.pessoa_fisica',),
        ),
        migrations.CreateModel(
            name='RegistroDiaAula',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia', models.CharField(choices=[('1', 'Segunda-Feira'), ('2', 'Terça-Feira'), ('3', 'Quarta-Feira'), ('4', 'Quinta-Feira'), ('5', 'Sexta-Feira'), ('6', 'Sábado'), ('7', 'Domingo')], max_length=1)),
                ('turma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academia.Aula')),
            ],
            options={
                'verbose_name': 'Registro_dias_Aulas_na_Semana',
                'verbose_name_plural': 'Registro_dias_Aulas_na_Semana',
                'db_table': 'dia_aula_semana',
            },
        ),
        migrations.CreateModel(
            name='RegistroAula',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia', models.DateField()),
                ('turma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academia.Aula')),
            ],
            options={
                'verbose_name': 'Confirmação_de_Aula',
                'verbose_name_plural': 'Confirmação_de_Aula',
                'db_table': 'registro_aula',
            },
        ),
        migrations.CreateModel(
            name='Parcela',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parcela', models.CharField(max_length=15)),
                ('dataInicio', models.DateField()),
                ('dataFim', models.DateField()),
                ('ferias', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='academia.Ferias')),
                ('matricula', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academia.Matricula')),
            ],
            options={
                'verbose_name': 'Parcelas_Férias',
                'verbose_name_plural': 'Parcelas_Férias',
                'db_table': 'parcela_ferias',
            },
        ),
        migrations.CreateModel(
            name='Pagamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referencia', models.CharField(default='6-2020', max_length=7)),
                ('data', models.DateField()),
                ('valor', models.FloatField()),
                ('matricula', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academia.Matricula')),
            ],
            options={
                'verbose_name': 'Pagamento',
                'verbose_name_plural': 'Pagamentos',
                'db_table': 'pagamento',
            },
        ),
        migrations.AddField(
            model_name='matricula',
            name='ferias',
            field=models.ManyToManyField(related_name='ferias', through='academia.Parcela', to='academia.Ferias'),
        ),
        migrations.AddField(
            model_name='matricula',
            name='plano',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academia.Plano'),
        ),
        migrations.CreateModel(
            name='Frequencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entrada', models.DateTimeField()),
                ('matricula', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academia.Matricula')),
                ('turma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academia.Aula')),
            ],
            options={
                'verbose_name': 'Frequência_Cliente',
                'verbose_name_plural': 'Frequência_Cliente',
                'db_table': 'frequencia_aluno',
            },
        ),
        migrations.AddField(
            model_name='plano',
            name='matriculas',
            field=models.ManyToManyField(related_name='matriculas', through='academia.Matricula', to='academia.Cliente'),
        ),
        migrations.AddField(
            model_name='matricula',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academia.Cliente'),
        ),
        migrations.CreateModel(
            name='Fisioterapeuta',
            fields=[
                ('pessoa_fisica_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='academia.Pessoa_Fisica')),
                ('registroConselho', models.CharField(max_length=45, primary_key=True, serialize=False)),
                ('avaliacoes', models.ManyToManyField(related_name='avaliacoes', through='academia.Avaliacao', to='academia.Cliente')),
            ],
            options={
                'verbose_name': 'Fisioterapeuta',
                'verbose_name_plural': 'Fisioterapeutas',
                'db_table': 'fisioterapeuta',
            },
            bases=('academia.pessoa_fisica',),
        ),
        migrations.AddField(
            model_name='avaliacao',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academia.Cliente'),
        ),
        migrations.AddField(
            model_name='avaliacao',
            name='fisioterapeuta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academia.Fisioterapeuta'),
        ),
        migrations.AddField(
            model_name='aula',
            name='instrutor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academia.Instrutor'),
        ),
    ]
