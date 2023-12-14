from django.shortcuts import render, redirect
import mysql.connector as sql
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.db import connection
# Create your views here.
from .forms import empdetails
from .models import getempdetails
from django.contrib.auth.hashers import make_password
from django.contrib import messages



id=''
fn=''
ln=''
s=''
em=''
pwd=''

# Create your views here.
def signaction(request):
    global fn,ln,s,em,pwd
    if request.method=="POST":
        m=sql.connect(host="localhost", user="root",passwd="", database='website_new')
        cursor=m.cursor()
        d=request.POST

        for key,value in d.items():
            if key=="empname":
                fn=value
            if key=="job":
                ln=value
            if key=="email":
                s=value
            if key=="username":
                em=value
            if key=="password":
                pwd=value
        try:
            user= User.objects.get(username=em)
            messages.error(request,"Maaf, username yang anda masukan sudah ada. Silahkan pilih username lain!")
            return render(request, 'signup_page.html')
        except User.DoesNotExist:
            user= User.objects.create_user(first_name=fn, last_name=ln, email=s, username=em, password=pwd)

        c="insert into getempdetails Values('{}','{}','{}','{}','{}','{}')".format(id,fn,ln,s,em,pwd)
        cursor.execute(c)
        m.commit()
        messages.success(request, "Create Account Successfully!")
    return render(request,'signup_page.html')

def loginaction(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index/') 
        else:
            msg = 'Error Login'
            form = AuthenticationForm(request.POST)
            return render(request, 'login_page.html', {'form': form, 'msg': msg})
    else:
        form = AuthenticationForm()
        return render(request, 'login_page.html', {'form': form})

def showDetails(request):
    cursor=connection.cursor()
    cursor.execute("call GetDataRecords()")
    result=cursor.fetchall()
    return render(request,'data-tabel.html',{'data_produk':result})
    
def user_index(request):
    return render(request,'index.html')

def user_profile(request):
    
    context = {}
    data = User.objects.filter(id=request.user.id)
    if request.POST.get("renewpassword") or request.POST.get("username") or request.POST.get("email") or request.POST.get("job") or request.POST.get("empname") == "":
        messages.error(request,"Please enter data correctly!")
        return render(request, 'user-profile.html')
    else:
        if len(data)>0:
            data = User.objects.get(id=request.user.id)
            context["data"] = data
            if request.method=="POST":
                fname = request.POST.get("empname")
                lname = request.POST.get("job")
                mail = request.POST.get("email")
                uname = request.POST.get("username")
                paswd = request.POST.get("renewpassword")

                usr = User.objects.get(id=request.user.id)
                usr.first_name = fname
                usr.last_name = lname
                usr.email = mail
                usr.username = uname
                usr.password = make_password(paswd)
                usr.save()
                context["Status"] = "Successfully Changed"
                print("Successfully Changed")
            
        return render(request,'user-profile.html', context)

def logout_request(request):
    logout(request)
    return redirect('/')

def data_tabel_qc(request):
    return render(request,'data-tabel.html')

def data_tabel_mesin(request):
    return render(request,'data-tabel-mesin.html')

def qc(request):
    return render(request,'parameter-qc.html')

def mesin(request):
    return render(request,'parameter-mesin.html')

def upld_csv(request):
    return render(request,'csvs/upload.html')

def update_user(request):
    return render(request,'user-profile.html')

