# Generated by Django 3.0.5 on 2020-04-03 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academia', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plano',
            name='tipo',
            field=models.CharField(choices=[('M', 'MENSAL'), ('A', 'ANUAL')], max_length=10, primary_key=True, serialize=False),
        ),
    ]
