# Generated by Django 5.0.3 on 2024-03-16 16:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('layouts', '0005_layout_account'),
    ]

    operations = [
        migrations.RenameField(
            model_name='layout',
            old_name='account',
            new_name='account_layout',
        ),
    ]