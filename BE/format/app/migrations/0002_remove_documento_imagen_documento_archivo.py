# Generated by Django 5.1.2 on 2024-10-30 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documento',
            name='imagen',
        ),
        migrations.AddField(
            model_name='documento',
            name='archivo',
            field=models.FileField(blank=True, null=True, upload_to='documentos/'),
        ),
    ]
