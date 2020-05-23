from django.shortcuts import render , redirect, get_object_or_404
from django.contrib.auth import authenticate , login
from .models import *
from django.http import Http404 , JsonResponse
from django.db.models import Q
from .filters import ProductFilter
import json


# Create your views here.
def home(request):
    products = Product.objects.all()[:3]
    context = {'products':products}
    return render(request, 'store/home.html', context)

def store(request):
    products = Product.objects.all()

    myFilter = ProductFilter(request.GET, queryset=products)

    products = myFilter.qs

    context = {
        'products': products, 'myFilter': myFilter
    }
    return render(request, 'store/listview.html', context)

def detailview(request, product_id):
    # try:
    #     product = Product.object.get(pk=product_id)
    # except Product.DoesNotExist:
    #     raise Http404("Product does not exist")    
    product = get_object_or_404(Product, pk=product_id)
    context = {
        'product': product
    }
  
    return render(request, 'store/detailview.html', context)    

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        return redirect('login')
        
    context = {'items':items , 'order':order}
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            print(items.count())
            if items.count() != 0:
                context = {'items': items , 'order': order}
                return render(request, 'store/checkout.html', context)
            else:
                return redirect('Store Home')
        else:
            return redirect('login')
    
    if request.method == 'POST':
        if request.user.is_authenticated:
            customer = request.user.customer
            order = Order.objects.get(customer=customer, complete=False)
            order.complete = True
            order.save()
            return redirect('Store Home')

def signup(request):
    if request.method == 'GET':
        return render(request, 'store/signup.html')

    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        name = request.POST["name"]
        email = request.POST["email"]
        address = request.POST["address"]
        city = request.POST["city"]
        phone_number = request.POST["phone_number"]

        user = User.objects.create_user(username , email , password)
        customer = Customer(user=user,name=name,email=email,address=address,city=city,phone_number=phone_number)
        customer.save()
        return redirect('Store Home')

def login_view(request):
    if request.method == 'GET':
        return render(request, 'store/login.html')

    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('Store Home')
        else:
            return render(request, 'store/login.html')

def category(request, category_name):
    products = Product.objects.filter(category=category_name)

    myFilter = ProductFilter(request.GET, queryset=products)

    products = myFilter.qs

    context = {
        'products': products, 'myFilter': myFilter,
    }
    return render(request, 'store/category.html', context)



def logout_view(request):
    logout(request)
    return redirect('Store Home')

def search(request):        
    if request.method == 'GET':    
        query =  request.GET.get('q')      
        try:
            products = Product.objects.filter(Q(title__icontains=query) | Q(brand__icontains=query)) 
        except Product.DoesNotExist:
            raise Http404("Product does not exist")  
        return render(request,"store/listview.html",{"products":products})

def updateitem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('product ID : ' , productId)
    print('Action : ' , action)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderitem , created = OrderItem.objects.get_or_create(order=order,product=product)

    if action == 'add':
        orderitem.quantity = orderitem.quantity + 1
    else:
        orderitem.quantity = orderitem.quantity - 1

    orderitem.save()
    if orderitem.quantity <= 0 :
        orderitem.delete()

    return JsonResponse('item was added' , safe=False)
