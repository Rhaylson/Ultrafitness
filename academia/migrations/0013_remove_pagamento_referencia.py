# Generated by Django 3.0.5 on 2020-04-07 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('academia', '0012_auto_20200407_1036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pagamento',
            name='referencia',
        ),
    ]