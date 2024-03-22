# Generated by Django 5.0.3 on 2024-03-21 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CloudOnSite', '0003_storageshelf'),
    ]

    operations = [
        migrations.CreateModel(
            name='CloudStorage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('storage', models.CharField(max_length=10)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('price_per_tb_transfer', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
