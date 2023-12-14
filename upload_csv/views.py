from django.shortcuts import render
from .forms import CsvModelForm
from .models import Csv
import csv
from django.contrib.auth.models import User
from data_parameter.models import data_produk
from django.contrib import messages
#from django.http import HttpResponse
# Create your views here.

def upload_file_view(request):

    form = CsvModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        form = CsvModelForm()
        obj = Csv.objects.get(activated=False)
        with open(obj.file_name.path, 'r') as f:
            reader = csv.reader(f)

            for i, row in enumerate(reader):
                if i==0:
                    pass
                else:
                    row = "".join(row)
                    row = row.replace(" ", "_")
                    row = row.replace(";", " ")
                    row = row.split()
                    uname= row[1].upper()

                    data_produk.objects.create(
                        product= row[0],
                        unit=uname,
                        kelembaban=row[2],
                        tekanan=row[3],
                        waktu=row[4],
                        suhu=row[5],
                        sudut=row[6],
                    )
                    # print(row)
                    # print(type(row))
            obj.activated = True
            obj.save()
            messages.success(request,"Save Berhasil!")
    return render(request, 'parameter-qc.html', {'form': form})
