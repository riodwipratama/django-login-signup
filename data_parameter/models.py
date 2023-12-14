from django.db import models

# Create your models here.

class getempdetails(models.Model):
    empname=models.CharField(max_length=100)
    job=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)

    class Meta:
        db_table = 'getempdetails'

class data_produk(models.Model):
    product = models.CharField(max_length=100)
    unit = models.CharField(max_length=100)
    kelembaban=models.FloatField()
    tekanan=models.FloatField()
    waktu=models.FloatField()
    suhu=models.FloatField()
    sudut=models.FloatField()

    def __str__(self):
        return f"{self.product}"