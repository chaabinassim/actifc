# Generated by Django 5.1.2 on 2025-01-23 16:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_project'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SupplyDemand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp when the supply demand was created.')),
                ('project', models.ForeignKey(help_text='Project related to this supply demand.', on_delete=django.db.models.deletion.CASCADE, related_name='supply_demands', to='inventory.project')),
                ('user', models.ForeignKey(help_text='User who created the supply demand.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Supply Demand',
                'verbose_name_plural': 'Supply Demands',
                'ordering': ['-created_at'],
                'permissions': [('view_own_supplydemand', 'Can view own supply demands')],
            },
        ),
        migrations.CreateModel(
            name='SupplyDemandItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(help_text='Quantity of the product requested.')),
                ('designation', models.CharField(help_text='Description of the product in case it is not in the product model.', max_length=255)),
                ('supply_demand', models.ForeignKey(help_text='Related supply demand.', on_delete=django.db.models.deletion.CASCADE, related_name='items', to='inventory.supplydemand')),
            ],
            options={
                'verbose_name': 'Supply Demand Item',
                'verbose_name_plural': 'Supply Demand Items',
            },
        ),
    ]
