from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import auth,User
from django.contrib.auth import login
from Ecommerce_App.models import Categories,Products,Users,Cart
import os
import re
from django.contrib.auth.decorators import login_required


# Create your views here.

def home(request):
    return render(request,'home.html')

@login_required(login_url='Log_In')
def store(request):
    cat5=Categories.objects.all()
    return render(request,'store.html',{'categories':cat5})

def contact_us(request):
    return render(request,'contact_us.html')

def Log_In(request):
    return render(request,'login.html')

def Fun_LogIn(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['pswd']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            if user.is_staff:
                login(request,user)
                return redirect('adminHome')
            else:
                auth.login(request,user)
                # messages.info(request,f'Welcome {username}! You have been Logged In')
                return redirect('userHome')
        else:
            messages.info(request,'Invalid Username or Password')
            return redirect('Log_In')
    return render(request,'login.html')

def adminHome(request):
    return render(request,'adminhome.html')

def categories(request):
    return render(request,'categories.html')

def add_categories(request):
    if request.method == 'POST':
        category_name=request.POST['category']
        cat=Categories(Category=category_name)
        cat.save()
        messages.info(request,'Category added Successfully')
        return redirect('categories')


def products(request):
    cat1=Categories.objects.all()
    return render(request,'products.html',{'categories':cat1})

def add_products(request):
    if request.method == 'POST':
        product_name=request.POST['pname']
        description=request.POST['desc']
        price=request.POST['price']
        category=request.POST['categories']
        catid=Categories.objects.get(id=category)
        image=request.FILES['img']
        prdt=Products(Product_name=product_name,Description=description,Price=price,Product_image=image,Category=catid)
        prdt.save()
        messages.info(request,'Product added succesfully')
        return redirect('products')
    
def view_products(request):
    prdt1=Products.objects.all()
    return render(request,'view_products.html',{'products':prdt1})

def edit_prdt(request,pd):
    prdt2=Products.objects.get(id=pd)
    cat3=Categories.objects.all()
    return render(request,'edit_products.html',{'products':prdt2,'category':cat3})

def edit_products(request,pd):
    if request.method == 'POST':
        prdt3=Products.objects.get(id=pd)
        prdt3.Product_name=request.POST['pname']
        prdt3.Description=request.POST['desc']
        prdt3.Price=request.POST['price']
        category=request.POST['categories']
        categoryid=Categories.objects.get(id=category)
        prdt3.Category=categoryid
        if 'img' in request.FILES:
            new_image = request.FILES['img']
            if prdt3.Product_image and os.path.exists(prdt3.Product_image.path):
                os.remove(prdt3.Product_image.path)
            prdt3.Product_image = new_image
        prdt3.save()
        return redirect('view_products')
    return render(request,'edit_products.html')

def delete_product(request,pd):
    delprdt=Products.objects.get(id=pd)
    if delprdt.Product_image and os.path.isfile(delprdt.Product_image.path):
        os.remove(delprdt.Product_image.path)
    delprdt.delete()
    return redirect('view_products')

def Log_Out(request):
    auth.logout(request)  
    return redirect('home')

def Sign_Up(request):
    return render(request,'user_signup.html')

def Fun_Signup(request):
    if request.method == 'POST':
        first_name=request.POST['fname']
        last_name=request.POST['lname']
        username=request.POST['username']
        password=request.POST['pswd']
        conf_password=request.POST['cfpswd']
        address=request.POST['address']
        email=request.POST['email']
        contact_number=request.POST['cnum']
        image=request.FILES['img']
        if password == conf_password:
            if User.objects.filter(username = username).exists():
                messages.info(request,'This Username already Exists..!!')
                return redirect('Sign_Up')
            
             # Phone number validation (10 digits)
            elif not re.match(r'^[0-9]{10}$', contact_number):
                messages.error(request, 'Invalid phone number! Please enter a valid 10-digit number.')
                return redirect('Sign_Up')

            # Email validation
            elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                messages.info(request, 'Invalid email address! Please enter a valid email address.')
                return redirect('Sign_Up')
            
            elif not re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$', password):
                messages.info(request, 'Invalid password! Password must be at least 6 characters long and contain at least one uppercase letter, one digit, and one special character.')
                return redirect('Sign_Up')
            
            else:
                user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
                user1=Users(Address=address,Contact_number=contact_number,Image=image,User=user)
                user1.save()
        else:
            messages.info(request,"Password doesn't Match.!!")
            return redirect('Sign_Up')
        return redirect('Log_In')

def view_users(request):
    user2=Users.objects.all()
    return render(request,'view_users.html',{'users':user2})

def delete_user(request,ud):
    users=Users.objects.get(id=ud) 
    user=users.User
    if users.Image and os.path.isfile(users.Image.path):
        os.remove(users.Image.path)
    users.delete()
    user.delete()
    return redirect('view_users')


def userHome(request):
    cart_counts=Cart.objects.filter(User=request.user).count()
    cart_count=cart_counts
    cat3=Categories.objects.all()
    return render(request,'userhome.html',{'categories':cat3,'item_counts':cart_count})

# def Gold(request):
#     cart_counts=Cart.objects.filter(User=request.user).count()
#     cart_count=cart_counts
#     cat4 = Categories.objects.all()
#     gold_category = Categories.objects.get(Category='Gold')
#     gold_products = Products.objects.filter(Category=gold_category)
#     return render(request, 'gold.html', {'categories': cat4, 'prdts': gold_products,'item_counts':cart_count})


# def Diamonds(request):
#     cart_counts=Cart.objects.filter(User=request.user).count()
#     cart_count=cart_counts
#     cat5=Categories.objects.all()
#     dia_category = Categories.objects.get(Category='Diamonds')
#     dia_products = Products.objects.filter(Category=dia_category)
#     return render(request,'diamonds.html',{'categories':cat5,'prdts':dia_products,'item_counts':cart_count})

# def Platinum(request):
#     cart_counts=Cart.objects.filter(User=request.user).count()
#     cart_count=cart_counts
#     cat6=Categories.objects.all()
#     plt_category = Categories.objects.get(Category='Platinum')
#     plt_products = Products.objects.filter(Category=plt_category)
#     return render(request,'platinum.html',{'categories':cat6,'prdts':plt_products,'item_counts':cart_count})

# def Silver(request):
#     cart_counts=Cart.objects.filter(User=request.user).count()
#     cart_count=cart_counts
#     cat7=Categories.objects.all()
#     sil_category = Categories.objects.get(Category='Silver')
#     sil_products = Products.objects.filter(Category=sil_category)
#     return render(request,'silver.html',{'categories':cat7,'prdts':sil_products,'item_counts':cart_count})


def navbar(request):
    categories = Categories.objects.all()  # Ensure this retrieves all categories
    return {'categories': categories}


def AllCollections(request, category_name):
    cart_count = Cart.objects.filter(User=request.user).count()
    categories = Categories.objects.all() 
    products = Products.objects.filter(Category__Category=category_name)

    return render(request, 'all_products.html', {'categories': category_name,'prdts': products,'item_counts': cart_count,'categories': categories})


def user_profile(request):
    cart_counts=Cart.objects.filter(User=request.user).count()
    cart_count=cart_counts
    cat3=Categories.objects.all()
    current_user=request.user.id
    prf=Users.objects.get(User_id=current_user)
    return render(request,'userprofile.html',{'user':prf,'categories':cat3,'item_counts':cart_count})

def edit_prf(request):
    cart_counts=Cart.objects.filter(User=request.user).count()
    cart_count=cart_counts
    cat4=Categories.objects.all()
    current_user=request.user.id
    prf=Users.objects.get(User_id=current_user)
    return render(request,'edit_profile.html',{'user':prf,'categories':cat4,'item_counts':cart_count})


def edit_profile(request):
    if request.method == 'POST':
        current_user = request.user.id
        user5 = Users.objects.get(User_id=current_user)
        user5.User.first_name = request.POST.get('fname')
        user5.User.last_name = request.POST.get('lname')
        user5.User.username = request.POST.get('username')
        user5.User.email = request.POST.get('email')
        user5.User.save()
        user5.Address = request.POST.get('address')
        user5.Contact_number = request.POST.get('cnum')
        if 'img' in request.FILES:
            new_image = request.FILES['img']
            if user5.Image and os.path.exists(user5.Image.path):
                os.remove(user5.Image.path)
            user5.Image = new_image
        
        user5.save()
        return redirect('user_profile')
    
def Cart_page(request):
    # Fetch all categories for display
    cat4 = Categories.objects.all()

    # Fetch all cart items for the logged-in user
    cart_items = Cart.objects.filter(User=request.user)

    # Calculate the total price of all valid items
    total = sum(float(item.Total_price()) for item in cart_items)

    # Get the count of cart items
    cart_count = cart_items.count()


    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total, 'categories': cat4, 'item_counts': cart_count})


def addto_cart(request,pd):
    prd_id=Products.objects.get(id=pd)
    # Get or create a cart item for the logged in user and the product
    cart_item , created =Cart.objects.get_or_create(User=request.user, Product=prd_id)
    if not created:
        # If the cart item already exists,increment the quantity
        cart_item.Quantity += 1
        cart_item.save()  #save the updated cart item
    return redirect('Cart_page')
    
def Increase_quantity(request, qd):
    cart_item = Cart.objects.get(User=request.user, Product=qd)  # Use get() to fetch the single item
    cart_item.Quantity += 1
    cart_item.save()
    return redirect('Cart_page')

def Decrease_quantity(request, qd):
    cart_item = Cart.objects.get(User=request.user, Product=qd)  # Use get() to fetch the single item
    if cart_item.Quantity > 1:  # Prevent decreasing below 1
        cart_item.Quantity -= 1
        cart_item.save()
    return redirect('Cart_page')

def deletecart_item(request,cd):
    cart_item=Cart.objects.filter(User=request.user,Product=cd)
    cart_item.delete()
    return redirect('Cart_page')

def Place_Order(request):
    categories = Categories.objects.all()
    cart_counts=Cart.objects.filter(User=request.user).count()
    cart_count=cart_counts
    return render(request, 'place_order.html', {'categories': categories,'item_counts': cart_count})


def modal_closeBtn(request):
    cart_item=Cart.objects.filter(User=request.user)
    cart_item.delete()
    return redirect('Cart_page')