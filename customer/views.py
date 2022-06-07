from multiprocessing import context
from django.shortcuts import render
from django.http import HttpResponse

from customer.models import Customer, Order, Product

# Create your views here.

def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'orders':orders, 'customers':customers, 'total_customers':total_customers, 'total_orders':total_orders, 'delivered':delivered, 'pending':pending}
    return render(request, 'customer/dashboard.html', context)

def products(request):
    products = Product.objects.all()
    return render(request, 'customer/products.html', {'products': products})

def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    total_order = orders.count()
    context = {'customer':customer, 'orders':orders, 'total_order':total_order}
    return render(request, 'customer/customer.html', context)
