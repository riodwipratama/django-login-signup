from django.db import models


# Create your models here.
class data_preparation(models.Model):
    id_product = models.CharField(max_length=100)
    unit_name = models.CharField(max_length=100)
    kel=models.FloatField()
    tek=models.FloatField()
    wkt=models.FloatField()
    sh=models.FloatField()
    sdt=models.FloatField()
    tsqr=models.FloatField()
    keterangan=models.CharField(max_length=100)
    d1=models.FloatField()
    d2=models.FloatField()
    d3=models.FloatField()
    d4=models.FloatField()
    variabel=models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id_product}"