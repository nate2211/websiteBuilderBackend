# Generated by Django 5.0.3 on 2024-03-16 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_rename_accountlayouts_accountlayout'),
        ('layouts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='layoutcomponent',
            name='images',
            field=models.ManyToManyField(related_name='components', to='accounts.accountimage'),
        ),
    ]