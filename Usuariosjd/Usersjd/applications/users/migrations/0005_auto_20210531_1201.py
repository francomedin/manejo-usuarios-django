# Generated by Django 3.2.3 on 2021-05-31 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_rename_gener_user_genero'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='cod_registro',
            field=models.CharField(blank=True, max_length=6),
        ),
        migrations.AddField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
