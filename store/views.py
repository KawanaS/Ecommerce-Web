from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from .models import *

# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'C:/Python/Django/ecommerce/store/templates/store/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('store')
        
def register(request):
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid(): 
                #saving the registered user
                user = form.save()
                Customer.objects.create(
                    user = user,
                    name = user.username,
                    email = user.email
                )    
                username= form.cleaned_data.get('username') 
                messages.success(request, f'Your Account has been created! You can now log in')
                return redirect('login')
        else:
            form = UserCreationForm() #creates an empty form
        return render(request, 'C:/Python/Django/ecommerce/store/templates/store/register.html', {'form': form})

def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items=[]
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']
    
    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    
    search_input = request.GET.get('search-area') or ''
    if search_input:
        context['products'] = context['products'].filter(name__icontains = search_input)
        
    context ['search_input'] = search_input
    
    return render(request, 'C:/Python/Django/ecommerce/store/templates/store/store.html',context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items=[]
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']
        
    context = {'items': items, 'order': order,'cartItems': cartItems}
    return render(request, 'C:/Python/Django/ecommerce/store/templates/store/cart.html',context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items=[]
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']
        
    context = {'items': items, 'order': order,'cartItems': cartItems}
    return render(request, 'C:/Python/Django/ecommerce/store/templates/store/checkout.html',context)


def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action: ', action)
    print('Product: ', productId)
    
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer,complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete
    
    return JsonResponse('Item has been added', safe=False)

def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.load(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        
        if total == float(order.get_cart_total):
            order.complete = True
        order.save()
    
    if order.shipping == True:
        ShippingAdress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            country = data['shipping']['country'],
            zipcode = data['shipping']['zipcode'],
            )
    
    else:
        print('User is not logged in!')
    return JsonResponse('Payment complete!', safe=False)
