from django.contrib import messages
from django.shortcuts import render, redirect
from .decorators import unauthenticated_user, allowed_users, admin_only
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerFrom
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group


@unauthenticated_user
def registrationPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            # getting data from a form
            username = form.cleaned_data.get('username')

            # a user is added to a group
            group = Group.objects.get(name='customer')
            user.groups.add(group)

            # customer giving a user
            Customer.objects.create(
                user=user
            )

            # do not have to pass it to the template, it temporally stored as a value
            messages.success(request, " successfully registered ", username)
            return redirect('login')

    context = {'form': form}
    return render(request, 'register.html', context)


@unauthenticated_user
def loginPage(request):
    # logged id user should not access the register
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "username or password incorrect")
    context = {}
    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    delivered = orders.filter(status='delivered').count()
    pending = orders.filter(status="pending").count()

    context = {'orders': orders,
               'total_orders': total_orders,
               'delivered': delivered,
               'pending': pending
               }
    return render(request, 'users.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    # get a user a any point in time
    cus = request.user.customer
    form = CustomerFrom(instance=cus)

    if request.method == 'POST':
        form = CustomerFrom(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'account_settings.html', context)


@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customer = customers.count()

    total_orders = orders.count()
    delivered = orders.filter(status='delivered').count()
    pending = orders.filter(status='pending').count()

    context = {'orders': orders,
               'customers': customers,
               'total_customer': total_customer,
               'total_orders': total_orders,
               'delivered': delivered,
               'pending': pending
               }
    return render(request, 'dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    product = Product.objects.all()
    context = {'products': product}
    return render(request, 'products.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)

    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {
        'customer': customer,
        'orders': orders,
        'order_count': order_count,
        'myFilter': myFilter,
    }
    return render(request, 'customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=3)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer': cus})

    if request.method == "POST":
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)

        if formset.is_valid():
            formset.save()
            messages.success(request, " submitted successfully")
            return redirect('/')

    context = {'formset': formset}
    return render(request, 'order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')
    context = {'order': order}
    return render(request, 'delete_order.html', context)
