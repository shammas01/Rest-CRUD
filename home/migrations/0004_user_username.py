# Generated by Django 4.2.3 on 2023-07-19 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_doctermodel_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]