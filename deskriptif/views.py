from django.shortcuts import render, redirect
from data_parameter.models import data_produk
from .models import data_preparation
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from django.conf import settings
from django.contrib import messages
import hotelling
from hotelling.plots import control_chart
from hotelling.stats import hotelling_t2
import warnings
warnings.simplefilter("ignore", UserWarning)
import dataframe_image as dfi
import csv
from django_pandas.io import read_frame




def getread(request):
    dframe=data_produk.objects.all()
    if not dframe.exists():
        messages.error(request,"Maaf, Anda belum bisa masuk menu ini! Silahkan input atau upload data terlebih dahulu")
        return redirect('csv_file')
    else:
        datas = data_produk.objects.all().values()
        df = pd.DataFrame(datas)
        my_dict = {
            "df" : df.to_html()
        }

        if 'id' in df.columns:
            df = df.drop(['id'], axis=1)

        dfi.export(df, os.path.join(settings.BASE_DIR, 'static/assets/img/dataframe.png'),max_rows=10)
        dfi.export(df.describe().T, os.path.join(settings.BASE_DIR, 'static/assets/img/describe.png'),max_rows=10)

        hub = ['kelembaban', 'tekanan', 'waktu', 'suhu']
        data = df[hub]
        sns.pairplot(data, hue ='kelembaban', kind ='scatter', palette = ('mako'))
        plt.savefig(os.path.join(settings.BASE_DIR, 'static/assets/img/scatter.png'))

        return deskriptif_page(request, datas, df, hub, data)



# Create your views here.
def deskriptif_page(request, datas, df, hub, data):


    # title = "Pearson Correlation"
    # plt.figure(figsize = (8,6))
    # sns.heatmap(df.corr(numeric_only = True), annot = True, cmap = 'YlGnBu')
    # plt.title("Pearson Correlation", fontsize = 15, color = 'b', pad = 12, loc = 'center')
    # plt.title(title)
    # plt.savefig(os.path.join(settings.BASE_DIR, 'static/assets/img/Pearson.png'))

    #plt.show()
    hub = ['kelembaban', 'tekanan', 'waktu', 'suhu']
    pic = df[hub].corr()
    title = "Pearson Correlation"
    plt.figure(figsize = (8,6))
    htmap = sns.heatmap(pic, vmin=-1, vmax=1, annot=True, cmap = sns.color_palette('mako'))
    plt.title("Correlation", fontsize = 15, color = 'b', pad = 12, loc = 'center')
    plt.title(title)
    plt.savefig(os.path.join(settings.BASE_DIR, 'static/assets/img/PearsonCorr.png'))
    miss=(df.isnull().sum().sort_values(ascending = False) * 100 / len(df)).round(2)
    context = {}
    context['baris'] = df.shape[0]
    context['kolom'] = df.shape[1]
    context['duplikasi'] = df.duplicated().sum()
    context['missing'] = sum(df.isna().sum())
    context['miss_id'] = "{0:.0f}%".format(miss[0] * 100)
    context['miss_unit'] = "{0:.0f}%".format(miss[1] * 100)
    context['miss_kelembaban'] = "{0:.0f}%".format(miss[2] * 100)
    context['miss_tekanan'] = "{0:.0f}%".format(miss[3] * 100)
    context['miss_waktu'] = "{0:.0f}%".format(miss[4] * 100)
    context['miss_suhu'] = "{0:.0f}%".format(miss[5] * 100)
    context['miss_sudut'] = "{0:.0f}%".format(miss[6] * 100)
    tipe_data = df.dtypes
    context['type'] = tipe_data[0]

    #Descriptive Analysis using Hotteling's T-Squared Control Chart

    if 'sudut' in df.columns:
        df = df.drop(['sudut'], axis=1)
    x = df[hub]
    xbar, s = hotelling.plots.control_stats(x)
    n = len(df.index)
    m = n
    f = len(df.select_dtypes(include=['float64']).columns)
    phase = 1
    alpha = 0.0026

    ucl, cl, lcl = hotelling.plots.control_interval(n, m, f, phase, alpha)

    #constant alpha for Type I Error --> alpha = 0.0026
    hotelling.plots.control_chart(x, phase=1, alpha=0.0026, width=18, marker="", interactive=False)
    plt.savefig(os.path.join(settings.BASE_DIR, 'static/assets/img/hotelling.png'))


    x = df[hub]
    fig, tsquared, ooc_df = hotelling.plots.control_chart(x, phase=1, alpha=0.0026, width=18, marker="")
    ooc_df = ooc_df.to_html()
    context['ooc_df'] = ooc_df

    df.insert(6, 'T-Squared', tsquared, True)

    exc_kelembaban = df[['tekanan','waktu','suhu']]
    exc_tekanan = df[['kelembaban','waktu','suhu']]
    exc_waktu = df[['tekanan','kelembaban','suhu']]
    exc_suhu = df[['tekanan','waktu','kelembaban']]

    fig, ts_k, a = hotelling.plots.control_chart(exc_kelembaban, phase=1, alpha=0.0026, width=18, marker="")
    fig, ts_t, a = hotelling.plots.control_chart(exc_tekanan, phase=1, alpha=0.0026, width=18, marker="")
    fig, ts_w, a = hotelling.plots.control_chart(exc_waktu, phase=1, alpha=0.0026, width=18, marker="")
    fig, ts_s, a = hotelling.plots.control_chart(exc_suhu, phase=1, alpha=0.0026, width=18, marker="")

    df.insert(7, 'D1', '', True)
    df.insert(8, 'D2', '', True)
    df.insert(9, 'D3', '', True)
    df.insert(10, 'D4', '', True)
    df.insert(11, 'Variabel Berpengaruh', '', True)

    for i in df.index:
        Di_k = float (df['T-Squared'][i] - ts_k.loc[i])
        df['D1'].loc[i] = Di_k

        Di_t = float (df['T-Squared'][i] - ts_t.loc[i])
        df['D2'].loc[i] = Di_t

        Di_w = float (df['T-Squared'][i] - ts_w.loc[i])
        df['D3'].loc[i] = Di_w

        Di_s = float (df['T-Squared'][i] - ts_s.loc[i])
        df['D4'].loc[i] = Di_s

        max_di = max (Di_k, Di_t, Di_w, Di_s)

        if max_di == Di_k:
            txt = 'Kelembaban'
        elif max_di == Di_t:
            txt = 'Tekanan'
        elif max_di == Di_w:
            txt = 'Waktu'
        else :
            txt = 'Suhu'

        df['Variabel Berpengaruh'].loc[i] = txt

    df.insert(7, 'keterangan', '')
    new_row = df['keterangan']
    for j in df.index: new_row.loc[j] = 'In Control'

    os.makedirs('static/assets/csv_output_file', exist_ok=True)
    df.to_csv('static/assets/csv_output_file/output_DataFrame.csv')

    from pandas.io import sql
    from sqlalchemy import create_engine

    engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                        .format(user="root",
                                pw="",
                                db="website"))
    df.to_sql(con=engine, name='deskriptif_data_preparation', if_exists='replace')




    return render(request,'deskriptif/deskriptif-analysis.html',context)
