from django.db import models

from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.TextField(null=True, blank=True)
    storage = models.BooleanField(default=False)
    computing = models.BooleanField(default=False)
    archiving = models.BooleanField(default=False)


class StorageServer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    disks2_5 = models.PositiveIntegerField(default=False)
    disks3_5 = models.PositiveIntegerField()
    ram = models.PositiveIntegerField()
    processors = models.PositiveIntegerField(max_length=3)
    raid5 = models.BooleanField(default=False)
    raid6 = models.BooleanField(default=False)


class StorageRam(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.PositiveIntegerField(default=False)
    latency = models.PositiveIntegerField(default=False)

    def __str__(self):
        return self.name


class StorageProc(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cores = models.PositiveIntegerField(default=False)
    threads = models.PositiveIntegerField(default=False)
    cache = models.PositiveIntegerField(default=False)
    compatible_ram = models.CharField(max_length=100, default=False)
    server_id = models.ManyToManyField(StorageServer)

    def __str__(self):
        return self.name


class StorageShelf(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    disks2_5 = models.PositiveIntegerField(default=False)
    disks3_5 = models.PositiveIntegerField(default=False)
    server_id = models.ManyToManyField(StorageServer)


class CloudStorage(models.Model):
    name = models.CharField(max_length=100)
    storage = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_tb_transfer = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
