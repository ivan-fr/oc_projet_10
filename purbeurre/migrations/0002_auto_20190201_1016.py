# Generated by Django 2.1.5 on 2019-02-01 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purbeurre', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='salt',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]