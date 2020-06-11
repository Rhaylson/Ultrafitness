# Generated by Django 3.0.5 on 2020-05-17 14:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academia', '0022_matricula_ferias'),
    ]

    operations = [
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
        migrations.AlterField(
            model_name='aula',
            name='instrutor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academia.Instrutor'),
        ),
        migrations.AlterField(
            model_name='avaliacao',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academia.Cliente'),
        ),
        migrations.AlterField(
            model_name='avaliacao',
            name='fisioterapeuta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academia.Fisioterapeuta'),
        ),
        migrations.AlterField(
            model_name='frequencia',
            name='matricula',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academia.Matricula'),
        ),
        migrations.AlterField(
            model_name='frequencia',
            name='turma',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academia.Aula'),
        ),
        migrations.AlterField(
            model_name='matricula',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academia.Cliente'),
        ),
        migrations.AlterField(
            model_name='matricula',
            name='plano',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academia.Plano'),
        ),
        migrations.AlterField(
            model_name='pagamento',
            name='matricula',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academia.Matricula'),
        ),
        migrations.AlterField(
            model_name='pagamento',
            name='referencia',
            field=models.CharField(default='5-2020', max_length=7),
        ),
        migrations.AlterField(
            model_name='parcela',
            name='ferias',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='academia.Ferias'),
        ),
        migrations.AlterField(
            model_name='parcela',
            name='matricula',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academia.Matricula'),
        ),
        migrations.AlterField(
            model_name='registroaula',
            name='turma',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academia.Aula'),
        ),
        migrations.AlterField(
            model_name='registrodiaaula',
            name='turma',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academia.Aula'),
        ),
        migrations.AlterField(
            model_name='pessoa_fisica',
            name='endereco',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='academia.Endereco'),
        ),
    ]
