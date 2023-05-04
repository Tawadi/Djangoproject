from django.shortcuts import redirect,render
from home.models import medicines
from home.models import *
#from locust import User
from django.contrib import messages
from django.contrib.auth import login,authenticate
from django.contrib.auth.models import User,auth 
from django.db.models import Q
from .models import Carts
from django.contrib.auth.decorators import login_required

from instamojo_wrapper import Instamojo
from django.conf import settings

api = Instamojo(api_key=settings.API_KEY,
                auth_token=settings.AUTH_TOKEN , endpoint="https://test.instamojo.com/api/1.1/")


# Create your views here.
def home(request):
    Medicines= medicines.objects.all()
    context={'Medicines':Medicines}
    print(context)
    return render(request,'home/home.html',context)

def about(request):
    context={'name':'tawadi','course':'django'}
    return render(request,  'home/about.html',context)

def contact(request):
    return render(request,'home/contact.html')

def project(request):
    return render(request,'home/project.html')

@login_required(login_url='/login/')
def add_cart(request , medicine_uid):
    user = request.user
    medicine_obj = medicines.objects.get(uid = medicine_uid)
    cart,_= Carts.objects.get_or_create(user = user, is_paid = False)
    cart_items = CartItems.objects.create(
        cart = cart,
        medicine = medicine_obj,
        )
    return redirect('/')

def login(request):
    if request.method == 'POST':
        username =request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('/login/')
    else:
        return render(request, 'home/login.html')
        
               
    
def register(request):
    if request.method == 'POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']   
        confirm_password=request.POST['confirm_password']
        if password==confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username is taken!')
                return redirect('/register/')
            user = User.objects.create_user(username=username, password=password,email=email,first_name=first_name,last_name=last_name)
            user.set_password(password)
            user.save()
            messages.info(request,'Account created successfully.')
            return redirect('/login/')
    else:
        print("something went wrong!")
        return render(request,'home/register.html')
        
def logout(request):
    auth.logout(request)
    return redirect('home')

def search(request):
    query=request.GET['search']
    allmedicines=medicines.objects.filter(medicine_name__icontains=query)
    params={'allmedicines':allmedicines,'query':query}
    return render(request,'home/search.html',params)
    
'''def search(request):
    query = request.GET.get('q') 
    results = []
    if query:
        results = medicines.objects.filter(medicine_name__icontains=query) 
    context = {'query': query, 'results': results}
    return render(request, 'home/search.html', context)'''
    
'''def search(request):
    query = request.GET.get('q')
    results = None
    if query is not None:
        results = medicines.objects.filter(Q(medicine_name__icontains=query))
        context = {'results': results,'query':query}
        if results is not None:
            return render(request, 'search_results.html', context)
        else:
            return render(request, 'home/search.html', context)'''


# def cart(request):
#     cart = Carts.objects.get(is_paid = False , user= request.user)
#     context={'carts': cart}
#     return render(request ,'home/cart.html', context)
@login_required(login_url='/login/')
def cart(request):
    cart = Carts.objects.get(is_paid=False, user=request.user)
    total = cart.get_cart_total()
    response = api.payment_request_create(
        amount = cart.get_cart_total(),
        purpose ="order",
        buyer_name = request.user.username,
        email= "tawadi1786@gmail.com",
        redirect_url ="http://127.0.0.1:8000/success/"
    )
    cart.instamojo_id= response['payment_request']['id']
    cart.save()
    context = {'cart': cart, 'total': total , 'payment_url': response['payment_request']['longurl']} 
    return render(request, 'home/cart.html', context)

@login_required(login_url='/login/')
def remove_cart_items(request ,cart_items_uid):
    try:
        CartItems.objects.get(uid =cart_items_uid).delete()

        return redirect('/cart/')
    except Exception as e:
        print(e)

@login_required(login_url='/login/')
def orders(request):
    orders = Carts.objects.filter(is_paid = True , user = request.user)
    context ={'orders' : orders}
    return render(request , 'home/orders.html' , context)

@login_required(login_url='/login/')
def success(request):
    payment_request= request.GET.get('payment_request_id')
    cart = Carts.objects.get(instamojo_id = payment_request)
    cart.is_paid = True
    cart.save()
    return redirect('/orders/')



