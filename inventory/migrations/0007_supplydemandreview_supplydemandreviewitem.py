# Generated by Django 5.1.2 on 2025-01-24 07:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_supplydemand_date_supplydemand_time'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SupplyDemandReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('time', models.TimeField(auto_now_add=True)),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL)),
                ('store', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviews', to='inventory.store')),
                ('supply_demand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='inventory.supplydemand')),
            ],
            options={
                'verbose_name': 'Supply Demand Review',
                'verbose_name_plural': 'Supply Demand Reviews',
                'ordering': ['-created_at'],
                'permissions': [('view_own_reviews', 'Can view own reviews'), ('view_supplydemandreviews_related_to_its_own_demands', 'Can view supply demand reviews related to its own demands')],
                'unique_together': {('supply_demand', 'store')},
            },
        ),
        migrations.CreateModel(
            name='SupplyDemandReviewItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requested_quantity', models.PositiveIntegerField(help_text='Quantity of the product requested.')),
                ('available_quantity', models.PositiveIntegerField(help_text='Quantity of the product available in stock.')),
                ('designation', models.CharField(help_text='Description of the product in case it is not in the product model.', max_length=255)),
                ('product', models.ForeignKey(blank=True, help_text='Product for the item. Can be null if product does not exist.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.product')),
                ('supply_demand_review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_items', to='inventory.supplydemandreview')),
            ],
            options={
                'verbose_name': 'Supply Demand Review Item',
                'verbose_name_plural': 'Supply Demand Review Items',
            },
        ),
    ]
