# Generated by Django 5.0.3 on 2024-03-10 23:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_accountlink'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='about',
            field=models.TextField(default='Codes a lot', max_length=2500, unique=True),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='DigitalProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
                ('file', models.FileField(upload_to='digital_products')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PhysicalProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
                ('weight', models.DecimalField(decimal_places=2, max_digits=6)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
