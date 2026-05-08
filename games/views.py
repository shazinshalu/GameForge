from django.shortcuts import render
from .models import *
from django.shortcuts import render,redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .models import User,products

from django.contrib import messages
def index(request):
    return render(request, 'index.html')
def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        if User.objects.filter(email=email).exists():
           messages.error(request, 'Email already registered.')
        else:
            User.objects.create(name=name, email=email, password=password, address=address, phone=phone)
            messages.success(request, 'registration successfull')
            return redirect ('index')
    return render(request,'register.html')
def login(request):
    if request.method =='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email, password=password)
            request.session['email'] = user.email
            messages.success(request, 'Login successful!')
            return redirect('index')
        except User.DoesNotExist:
            return render(request, 'login.html', {'error':'Invalid email or password.'})
    return render(request, 'login.html')
def profile(request):
    email = request.session.get('email')
    
    if email is not None:
        try:
            user = User.objects.get(email=email)
            return render(request, 'profile.html', {'user':user})
        except User.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('login')
    else:
        messages.warning(request, "You need to log in to access your profile.")
        return redirect('login')
def editprofile(request):
    email = request.session.get('email') 
    user = User.objects.get(email=email)  # Get the User object
    if request.method == 'POST':
        # Get the form data
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        location = request.POST.get('location')
        user.name = name
        user.phone = phone
        user.address = location
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')  
    return render(request, 'profile.html', {'user': user})
def userlist(request):
    user=User.objects.all()
    return render(request,'userlist.html',{'user':user})
def deleteuser(request,id):
    data=User.objects.filter(id=id)
    data.delete()
    return redirect('userlist')
def product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        category = request.POST.get('category')
        image = request.FILES.get('image')
        products.objects.create(name=name,price=price,quantity=quantity,category=category,description=description,image=image)
        messages.success(request, 'registration successfull')
        return redirect ('index')
    return render(request, 'products.html')
def product_list(request):
    p = products.objects.all()
    return render(request, 'productlist.html', {'p': p})
from django.http import JsonResponse
def edit_product(request, id):
    if request.method == "POST":
        product = get_object_or_404(products, id=id)

        try:
            product.name = request.POST.get('name')
            product.description = request.POST.get('description')
            product.price = request.POST.get('price')  # DecimalField → no int()
            product.quantity = int(request.POST.get('quantity'))
            product.category = request.POST.get('category')

            # ✅ update image only if new one is uploaded
            if request.FILES.get('image'):
                product.image = request.FILES.get('image')

            product.save()

            return JsonResponse({'success': True})

        except Exception as e:
            print("ERROR:", e)
            return JsonResponse({'success': False})

    return JsonResponse({'success': False})
def delete_product(request,id):
    data=products.objects.filter(id=id)
    data.delete()
    return redirect('productlist')
def add_to_cart(request, id): 
    product = get_object_or_404(products, id=id) 
    email = request.session.get('email') 
    if email: 
        user = get_object_or_404(User, email=email) 
        cart_item, created = Cart.objects.get_or_create( 
            user=user, 
            product=product, 
            defaults={'quantity': 1} 
        ) 
        if not created: 
            cart_item.quantity += 1 
            cart_item.total_price = cart_item.quantity * product.price 
            cart_item.save() 
        return redirect('cart')  # Replace 'view_cart' with your cart view name 
    else: 
        return JsonResponse({'authentication failed': 'User email not found in session. Please login first.'}, status=400)
def add_to_cart(request, id): 
    product = get_object_or_404(products, id=id) 
    email = request.session.get('email') 
    if email: 
        user = get_object_or_404(User, email=email) 
        cart_item, created = Cart.objects.get_or_create( 
            user=user, 
            product=product, 
            defaults={'quantity': 1} 
        ) 
        if not created: 
            cart_item.quantity += 1 
            cart_item.total_price = cart_item.quantity * product.price 
            cart_item.save() 
        return redirect('cart')  # Replace 'view_cart' with your cart view name 
    else: 
        return JsonResponse({'authentication failed': 'User email not found in session. Please login first.'}, status=400) 

def cart(request): 
     email = request.session.get('email') 
     if email: 
        user = get_object_or_404( User,email=email) 
        cart_items = Cart.objects.filter(user=user)
        for item in cart_items: 
            item.total_price = item.product.price * item.quantity 
     
        total_price = sum(item.total_price for item in cart_items) 
     
        return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price}) 
     else: 
        return render(request, 'cart.html', {'AUTHENTICATION FAILED': 'User email not found in session. Please login first.'}) 
def delete_cart(request, id):
    if request.method == "POST":
        cart_item = get_object_or_404(Cart, id=id) 
        cart_item.delete() 
        return redirect('cart') 
    return render(request, 'cart.html')
    
def userproduct_list(request):
    p = products.objects.all()
    return render(request, 'userproductlist.html', {'p': p})
def add_to_wishlist(request, id):
    product = get_object_or_404(products, id=id)
    email = request.session.get('email')

    if email:
        user = get_object_or_404(User, email=email)

        wishlist.objects.get_or_create(
            user=user,
            product=product,
        )

        return redirect('viewwishlist')

    else:
        return JsonResponse(
            {'error': 'User not logged in'},
            status=400
        )
def viewwishlist(request): 
     email = request.session.get('email') 
     if email: 
        user = get_object_or_404( User,email=email) 
        wishlist_items = wishlist.objects.filter(user=user)
     
        return render(request, 'wishlist.html', {'wishlist_items': wishlist_items}) 
     else: 
        return render(request, 'wishlist.html', {'AUTHENTICATION FAILED': 'User email not found in session. Please login first.'})

def feedback(request):
    email = request.session.get('email')
    if not email:
        return redirect('/login')  # 
    user = User.objects.filter(email=email).first()
    if request.method == "POST":
        feedback_text = request.POST.get('feedback_text')
        rating = request.POST.get('rating')

        # Check for missing fields
        if not feedback_text or not rating:
            return HttpResponse("<script>alert(' fill in all fields.'); window.location.href='/feedback_rate';</script>")
        try:
            rating = int(rating)
            if rating not in [1, 2, 3, 4, 5]:
                raise ValueError("Invalid rating value")
        except (ValueError, TypeError):
            return HttpResponse("<script>alert('Please select a valid rating.'); window.location.href='/feedback_rate';</script>")
        Feedback.objects.create(
            feedback_text=feedback_text,
            rating=rating,
            email=email  # Save the email from the session
        )
        return HttpResponse("<script>alert('Feedback submitted successfully!'); window.location.href='/index/';</script>")
    return render(request, 'feedback.html', {'e': user}) 

def about(request):
    return render(request, 'about.html')
def faq(request):
    return render(request, 'faq.html')
