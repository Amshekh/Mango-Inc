from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django.db.models import Q
import json
from cart.cart import Cart   # from folder 'cart' there is 'cart.py' & from there import 'Cart'

def search(request):
    if request.method == "POST":
        searched = request.post['searched']
        searched = Product.objects.filter(Q(name__icontains= searched) | Q(description__icontains= searched))
        if not searched:
            messages.success(request, ("No such product, try again !!!"))
            return render(request, 'search.html', {})
        else:
            return render(request, 'search.html', {'searched': searched})
    else:
        return render(request, 'search.html', {})

def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id) # Getting current user
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id) # Getting current user's shipping info
        form = UserInfoForm(request.POST or None, instance = current_user) # Getting original User form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)    # Getting User's shipping form

        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()

            messages.success(request, ("Your Profile Information has been updated !!!"))
            return redirect('home')
        
        return render(request, 'update_info.html', {"form": form, "shipping_form": shipping_form })
    
    else:
        messages.success(request, ("You must be Logged in to update your profile. . ."))
        return redirect('home')


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':  # Checking if user has filled Update Profile form
            #Perform action
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid:
                form.save()
                messages.success(request, ("Your password has been updated. . ."))
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:  
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form': form})
    else:
        messages.success(request, ("Log in to view the webpage"))
        return redirect('home')


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance = current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, ("User Profile has been updated !!!"))
            return redirect('home')
        
        return render(request, 'update_user.html', {"user_form": user_form})
    
    else:
        messages.success(request, ("You must be Logged in to update your profile. . ."))
        return redirect('home')
    

def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {"categories": categories})    

def category(request, cat):
    cat = cat.replace('-', ' ')  # Replacing hyphens in category names with space. e.g. mobile-phones  with mobile phones

    try:                             # Grab the category from the url
        category = Category.objects.get(name=cat)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products, 'category': category})
    except:
        messages.success(request, ("Category does not exist"))  
        return redirect('home')

def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            current_user = Profile.objects.get(user__id=request.user.id)
            saved_cart = current_user.previous_cart    # Getting the saved cart from database
            if saved_cart:    
                cart_dict = json.loads(saved_cart)  # Typecast or Convert string from database to Python Dictionary
                cart = Cart(request)  # Getting the cart
                for key, value in cart_dict.items():    # Looping through the cart and add the items from database
                    cart.db_add(product=key, quantity=value) # db_add is a function we are specifically creating to add to database

            messages.success(request, ("You have logged in !!!"))
            return redirect('home')
        else:
            messages.success(request, ("Please check your username or password to log in"))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You have successfully logged out !!!"))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You have Registered successfully.Complete your Profile info. . ."))
            return redirect('update_info')
        else:
            messages.error(request, ("There was a problem! retry with valid credentials"))
            return redirect('register')
    return render(request, 'register.html', {'form': form})