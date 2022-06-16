from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory                #InlineFormsets
from django.contrib import messages                           #Flash messages
from django.contrib.auth import authenticate, login, logout   #Authentication
from django.contrib.auth.decorators import login_required     #Login required decorator
from django.contrib.auth.models import Group

from customer.models import Customer, Order, Product, Tag
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only

# Create your views here.

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            group = Group.objects.get(name='customers')   
            user.groups.add(group)                              #Adding the user to the group         
            Customer.objects.create(user=user,)                 #When a user is registered, a Customer is being registered at the same time

            username = form.cleaned_data.get('username')        #Way of accessing form data
            messages.success(request, 'Account created successfully' + username)  #Flash messages

            return redirect('customer:login')
    context = {'form':form}
    return render(request, 'customer/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')               #Another way of accessing form data
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        # if user:
        #     login(request, user)
        #     return redirect('/')
        else:
            messages.info(request, 'Username or password is incorrect')
    context = {}
    return render(request, 'customer/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('customer:login')


@login_required(login_url='/login')
@allowed_users(allowed_roles=['customers'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'orders':orders, 'total_orders':total_orders, 'delivered':delivered, 'pending':pending}
    return render(request, 'customer/user.html', context)


@login_required(login_url='/login')
@allowed_users(allowed_roles=['customers'])
def accountSettings(request):
    form = CustomerForm(instance=request.user.customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=request.user.customer)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'customer/account_settings.html', context)



@login_required(login_url='/login')
# @allowed_users(allowed_roles=['admin'])
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'orders':orders, 'customers':customers, 'total_customers':total_customers, 'total_orders':total_orders, 'delivered':delivered, 'pending':pending}
    return render(request, 'customer/dashboard.html', context)



@login_required(login_url='/login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    return render(request, 'customer/products.html', {'products': products})



@login_required(login_url='/login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    total_order = orders.count()
    # django-filter
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    context = {'customer':customer, 'orders':orders, 'total_order':total_order, 'myFilter':myFilter}
    return render(request, 'customer/customer.html', context)



@login_required(login_url='/login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=5)   
    customer = Customer.objects.get(id=pk)
    # form = OrderForm(initial={'customer':customer})
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    if request.method == 'POST':
        # form = OrderForm(request.POST)
        # if form.is_valid():
        #     form.save()

        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()

            return redirect('/')
    # context = {'form':form}
    context = {'formset':formset}
    return render(request, 'customer/order_form.html', context)



@login_required(login_url='/login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request, 'customer/order_form.html', context)



@login_required(login_url='/login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'order':order}
    return render(request, 'customer/delete.html', context)
