# Generated by Django 2.2.5 on 2020-04-06 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covid19', '0010_auto_20200405_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticia',
            name='imagen',
            field=models.FileField(default='', upload_to='news/%Y/%m/%d/'),
            preserve_default=False,
        ),
    ]