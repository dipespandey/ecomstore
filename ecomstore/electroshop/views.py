import random
import decimal
from electroshop.models import Product,Category,UserProfile,CartItem,Cart
from django.shortcuts import render,get_object_or_404
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from electroshop.forms import UserForm, UserProfileForm,AddtoCartForm, DeliverProductForm



def product_list(request):
    categories = Category.objects.all()
    products = Product.objects.all()    
    return render(request,'electroshop/product_list.html',{'products':products, 'categories':categories})


def category_list(request,slug):
    category = Category.objects.get(slug=slug)
    products = category.product_set.get_queryset()
    return render(request,'electroshop/categories.html', {'category':category, 'products':products,})


# contains the detail page of the products along with add_to_cart feature
def product_detail(request,slug):
    try:
        product = Product.objects.get(slug=slug)

        if request.method=='POST':
            if request.user.is_authenticated():

                form = AddtoCartForm(data = request.POST)
                 
                if form.is_valid():

        #            # add the product to the cart
                    add_to_cart(request,slug)
        #             quantity = request.POST.get('quantity',1)


        #         

        #             product_in_cart = False
        #             cart_products = get_cart_items(request)

        #             #check for already existing items
        #             for cart_item in cart_products:
        #                 if cart_item.product.slug == product.slug:
        #                     cart_item.augment_quantity(quantity)


        #             if not product_in_cart:
        #                 ci = CartItem()
        #                 ci.product = product
        #                 ci.user = request.user
        #                 ci.quantity = quantity
        #                 ci.save()
        #             else:
        #                 HttpResponse("Item already in cart.")


        #             if request.session.test_cookie_worked():
        #                 request.session.delete_test_cookie()
        #                 return HttpResponseRedirect('electroshop/dashboard.html')
            else:
                return HttpResponse("You must login first")
        
        else:
            form = AddtoCartForm()

    except Product.DoesNotExist:
        raise Http404("Product does not exist")


    return render(request,'electroshop/product_detail.html',{'product':product, 'form':form,})



def search_product(request):
    query = request.POST.get('q','')
    exclude = [' ']
    if query:
        qset = (
            Q(name__icontains = query)
                       
        )
        results = Product.objects.filter(qset)
    else:
        results = []

    return render(request,'electroshop/search_product.html',{'results':results, 'query':query})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username,password=password)

        if not user.is_staff and not user.is_superuser:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect('Your ElectroShop Account has been disabled.')
        
        else:
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request,'electroshop/login.html',{})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def register(request):
    
    registered = False

    if request.method =='POST':
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileForm(data = request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)
        
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'electroshop/register.html',{'user_form':user_form, 'profile_form':profile_form,'registered':registered})


@login_required
def dashboard(request):
    user = User.objects.get(username = request.user.username)        
    profile = user.userprofile
    my_cart = CartItem.objects.all()


    total = 0
    for item in my_cart:
        total += item.product.price

    if request.method == 'POST':
        form = DeliverProductForm(data=request.POST)
        if form.is_valid():
            f = form.save()
            f.save()
    else:
        form = DeliverProductForm()

    return render(request,'electroshop/dashboard.html', {'user':user, 'profile':profile, 'my_cart':my_cart, 'total':total,'form':form})



# returns the total no. of items in the user's cart
def cart_distinct_item_count(request):
    return get_cart_items(request).count()



def get_cart_items(request):
    return CartItem.objects.all()


def add_to_cart(request, slug):

    if request.user.is_authenticated():   
        request.session.set_expiry(120000)

        try:
            the_id = request.session.get('cart_id',1)

        except:
            new_cart = Cart()
            new_cart.save()
            request.session['cart_id'] = new_cart.cart_id
            the_id = new_cart.id 

        cart = Cart.objects.get(id=the_id)

        try:
            product = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            pass
        except:
            pass

        if request.method == 'POST':
            qty = request.POST['quantity']

            cart_item = CartItem.objects.create(cart=cart, product=product)
            cart_products = get_cart_items(request)
            cart_item.augment_quantity(qty)

            cart_item.quantity = qty
            cart_item.save()
    else:
        return HttpResponse("You must login first")



