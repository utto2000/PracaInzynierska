# Generated by Django 5.0.3 on 2024-03-21 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CloudOnSite', '0002_storageram_storageserver_storageproc'),
    ]

    operations = [
        migrations.CreateModel(
            name='StorageShelf',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('disks2_5', models.PositiveIntegerField(default=False)),
                ('disks3_5', models.PositiveIntegerField(default=False)),
                ('server_id', models.ManyToManyField(to='CloudOnSite.storageserver')),
            ],
        ),
    ]
