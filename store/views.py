from enum import unique
from unicodedata import category
from django import http
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import *
import random
import json


def loginPage(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username:
            user_name = '\"'+username+'\"'
        else:
            user_name = username

        try:
            user = User.objects.get(username=username)
            print(user)
        except:
            messages.error(request, 'Username '+user_name+' does not exist')

        user = authenticate(User, username=username, password=password)
        if user != None:
            login(request, user)
            return redirect('home')
    context = {'page': page}
    return render(request, 'store/login-register.html', context)


def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        try:
            if form.is_valid:
                user = form.save(commit=False)
                user.save()
                login(request, user)
                return redirect('home')
        except:
            messages.error(
                request, 'An error occured while creating an account. Try again')
    context = {'form': form}
    return render(request, 'store/login-register.html', context)


def logoutPage(request):
    logout(request)
    return redirect('home')


def home(request):
    if request.method == 'POST':
        q = request.POST.get('q') if request.POST.get('q') != None else ''
    if request.method == 'GET':
        q = request.GET.get('q') if request.GET.get('q') != None else ''
    categories = Category.objects.all()
    products = Product.objects.filter(
        Q(name__icontains=q) |
        Q(product_cat__icontains=q) |
        Q(category__name__icontains=q)
    )
    products = list(products)
    # random.shuffle(products)
    pr = Category.objects.get(id=3)
    product_categories = pr.product_set.all().values('product_cat').distinct()
    # product_categories = Product.objects.all().values('product_cat').distinct()
    tshirt = Product.objects.filter(product_cat='t-shirt')[0:1]
    pant = Product.objects.filter(product_cat='pant')[0:1]

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartitems = order['get_cart_items']

    context = {'products': products, 'categories': categories,
               'product_categories': product_categories, 'tshirt1': tshirt, 'pant': pant,
               'cartitems': cartitems}
    return render(request, 'store/home.html', context)


@login_required(login_url='login')
def product(request, pk):
    product = Product.objects.get(id=pk)
    reviews = product.reviews_set.all()
    products = Product.objects.filter()[0:6]

    print(request.POST.get('body'))
    if request.POST.get('body') == '':
        pass
    else:
        if request.method == 'POST':
            reviews = Reviews.objects.create(
                product=product,
                user=request.user,
                body=request.POST.get('body')
            )
            return redirect('products', pk=product.id)

    context = {'product': product, 'products': products, 'reviews': reviews}
    return render(request, 'store/products.html', context)


def deleteReview(request, pk):
    q = request.GET.get('q')
    product = Product.objects.get(id=q)
    reviews = Reviews.objects.get(id=pk)

    if request.user != reviews.user:
        return HttpResponse("you cannot delete")

    if request.method == 'GET':
        reviews.delete()
        return redirect('products', pk=q)


def cartPage(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartitems = order['get_cart_items']
    context = {'items': items, 'order': order, 'cartitems': cartitems}
    return render(request, 'store/cart.html', context)


def updateItem(request):
    data = json.loads(request.body)
    action = data['action']
    product_id = data['product']

    if request.user.is_authenticated:
        customer = request.user.customer
        product = Product.objects.get(id=product_id)
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        orderitems, created = Orderitem.objects.get_or_create(
            order=order, product=product
        )

    if action == 'add':
        orderitems.quantity = (orderitems.quantity+1)
    elif action == 'remove':
        orderitems.quantity = (orderitems.quantity-1)

    orderitems.save()

    if orderitems.quantity <= 0:
        orderitems.delete()

    return JsonResponse('Hi', safe=False)


def deleteItem(request):
    data = json.loads(request.body)
    delete_item = data['delete_item']
    product_id = data['product_id']

    if request.user.is_authenticated:
        customer = request.user.customer
        product = Product.objects.get(id=product_id)
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        orderitems, created = Orderitem.objects.get_or_create(
            order=order, product=product
        )

    if delete_item == 'delete':
        orderitems.delete()
    return JsonResponse('deleted', safe=False)


def aboutUs(request):
    return render(request, 'store/about-us.html')


def contactUs(request):
    return render(request, 'store/contact.html')
