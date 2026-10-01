from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
import razorpay

from .models import (
    Customer,
    Restaurant,
    Menu,
    Cart,
    ContactMessage,
    Order,
    OrderItem
)


# ================= HOME =================

def index(request):

    return render(
        request,
        'delivery/index.html'
    )


# ================= ABOUT =================

def about(request):

    return render(
        request,
        'delivery/about.html'
    )


# ================= CONTACT =================

def contact(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        ContactMessage.objects.create(
            name=name,
            email=email,
            message=message
        )

        return render(
            request,
            'delivery/contact.html',
            {
                'success':
                    'Your message has been sent successfully!'
            }
        )

    return render(
        request,
        'delivery/contact.html'
    )


# ================= LOGOUT =================

def logout(request):

    return redirect('index')


# ================= SIGN UP =================

def open_signup(request):

    return render(
        request,
        'delivery/signup.html'
    )


def signup(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')

        if Customer.objects.filter(
            username=username
        ).exists():

            return HttpResponse(
                "Duplicate username!"
            )

        Customer.objects.create(
            username=username,
            password=password,
            email=email,
            mobile=mobile,
            address=address
        )

        return redirect(
            'open_signin'
        )

    return render(
        request,
        'delivery/signup.html'
    )


# ================= SIGN IN =================

def open_signin(request):

    return render(
        request,
        'delivery/signin.html'
    )


def signin(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        try:

            Customer.objects.get(
                username=username,
                password=password
            )

            if username == 'admin':

                return render(
                    request,
                    'delivery/admin_home.html'
                )

            else:

                restaurantList = Restaurant.objects.all()

                return render(
                    request,
                    'delivery/customer_home.html',
                    {
                        'restaurantList':
                            restaurantList,

                        'username':
                            username
                    }
                )

        except Customer.DoesNotExist:

            return HttpResponse(
                "Invalid username or password"
            )

    return render(
        request,
        'delivery/signin.html'
    )


# =========================================================
# ADMIN - RESTAURANT
# =========================================================

def open_add_restaurant(request):

    return render(
        request,
        'delivery/add_restaurant.html'
    )


def add_restaurant(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        picture = request.POST.get('picture')
        cuisine = request.POST.get('cuisine')
        rating = request.POST.get('rating')

        if Restaurant.objects.filter(
            name=name
        ).exists():

            return HttpResponse(
                "Duplicate restaurant!"
            )

        Restaurant.objects.create(
            name=name,
            picture=picture,
            cuisine=cuisine,
            rating=rating
        )

        return redirect(
            'open_show_restaurant'
        )

    return render(
        request,
        'delivery/add_restaurant.html'
    )


def open_show_restaurant(request):

    restaurantList = Restaurant.objects.all()

    return render(
        request,
        'delivery/show_restaurant.html',
        {
            'restaurantList':
                restaurantList
        }
    )


def open_update_restaurant(
    request,
    restaurant_id
):

    restaurant = Restaurant.objects.get(
        id=restaurant_id
    )

    return render(
        request,
        'delivery/update_restaurant.html',
        {
            'restaurant':
                restaurant
        }
    )


def update_restaurant(
    request,
    restaurant_id
):

    restaurant = Restaurant.objects.get(
        id=restaurant_id
    )

    if request.method == 'POST':

        restaurant.name = request.POST.get(
            'name'
        )

        restaurant.picture = request.POST.get(
            'picture'
        )

        restaurant.cuisine = request.POST.get(
            'cuisine'
        )

        restaurant.rating = request.POST.get(
            'rating'
        )

        restaurant.save()

        return redirect(
            'open_show_restaurant'
        )

    return render(
        request,
        'delivery/update_restaurant.html',
        {
            'restaurant':
                restaurant
        }
    )


def delete_restaurant(
    request,
    restaurant_id
):

    restaurant = Restaurant.objects.get(
        id=restaurant_id
    )

    restaurant.delete()

    return redirect(
        'open_show_restaurant'
    )


# =========================================================
# ADMIN - MENU
# =========================================================

def open_update_menu(
    request,
    restaurant_id
):

    restaurant = Restaurant.objects.get(
        id=restaurant_id
    )

    if request.method == 'POST':

        food_name = request.POST.get(
            'food_name'
        )

        description = request.POST.get(
            'description'
        )

        price = request.POST.get(
            'price'
        )

        picture = request.POST.get(
            'picture'
        )

        is_veg = request.POST.get(
            'is_veg'
        ) == 'on'

        Menu.objects.create(
            restaurant=restaurant,
            food_name=food_name,
            picture=picture,
            description=description,
            price=price,
            is_veg=is_veg
        )

        return redirect(
            'open_update_menu',
            restaurant_id=restaurant.id
        )

    menuList = Menu.objects.filter(
        restaurant=restaurant
    )

    return render(
        request,
        'delivery/update_menu.html',
        {
            'restaurant':
                restaurant,

            'menuList':
                menuList
        }
    )


def delete_menu(
    request,
    menu_id
):

    menu = Menu.objects.get(
        id=menu_id
    )

    restaurant_id = menu.restaurant.id

    menu.delete()

    return redirect(
        'open_update_menu',
        restaurant_id=restaurant_id
    )


# =========================================================
# CUSTOMER - VIEW MENU
# =========================================================

def view_menu(
    request,
    restaurant_id,
    username
):

    restaurant = Restaurant.objects.get(
        id=restaurant_id
    )

    menuList = Menu.objects.filter(
        restaurant=restaurant
    )

    cart_items = Cart.objects.filter(
        username=username
    )

    for menu in menuList:

        try:

            cart_item = Cart.objects.get(
                username=username,
                menu=menu
            )

            menu.cart_quantity = (
                cart_item.quantity
            )

        except Cart.DoesNotExist:

            menu.cart_quantity = 0

    return render(
        request,
        'delivery/view_menu.html',
        {
            'restaurant':
                restaurant,

            'menuList':
                menuList,

            'username':
                username
        }
    )


# =========================================================
# ADD TO CART
# =========================================================

def add_to_cart(
    request,
    menu_id,
    restaurant_id,
    username
):

    menu = Menu.objects.get(
        id=menu_id
    )

    try:

        cart_item = Cart.objects.get(
            username=username,
            menu=menu
        )

        cart_item.quantity = (
            cart_item.quantity + 1
        )

        cart_item.save()

    except Cart.DoesNotExist:

        Cart.objects.create(
            username=username,
            menu=menu,
            quantity=1
        )

    return redirect(
        'view_menu',
        restaurant_id=restaurant_id,
        username=username
    )


# =========================================================
# CART
# =========================================================

def cart(
    request,
    username
):

    cart_items = Cart.objects.filter(
        username=username
    )

    menuList = []

    total = 0

    for cart_item in cart_items:

        item_total = (
            cart_item.menu.price
            * cart_item.quantity
        )

        total = total + item_total

        menuList.append(
            {
                'menu':
                    cart_item.menu,

                'quantity':
                    cart_item.quantity,

                'item_total':
                    item_total
            }
        )

    return render(
        request,
        'delivery/cart.html',
        {
            'menuList':
                menuList,

            'total':
                total,

            'username':
                username
        }
    )


# =========================================================
# REMOVE FROM CART
# =========================================================

def remove_from_cart(
    request,
    menu_id,
    username
):

    menu = Menu.objects.get(
        id=menu_id
    )

    Cart.objects.filter(
        username=username,
        menu=menu
    ).delete()

    return redirect(
        'cart',
        username=username
    )


# =========================================================
# INCREASE QUANTITY
# =========================================================

def increase_cart(
    request,
    menu_id,
    username
):

    menu = Menu.objects.get(
        id=menu_id
    )

    try:

        cart_item = Cart.objects.get(
            username=username,
            menu=menu
        )

        cart_item.quantity = (
            cart_item.quantity + 1
        )

        cart_item.save()

    except Cart.DoesNotExist:

        pass

    return redirect(
        'cart',
        username=username
    )


# =========================================================
# DECREASE QUANTITY
# =========================================================

def decrease_cart(
    request,
    menu_id,
    username
):

    menu = Menu.objects.get(
        id=menu_id
    )

    try:

        cart_item = Cart.objects.get(
            username=username,
            menu=menu
        )

        cart_item.quantity = (
            cart_item.quantity - 1
        )

        if cart_item.quantity <= 0:

            cart_item.delete()

        else:

            cart_item.save()

    except Cart.DoesNotExist:

        pass

    return redirect(
        'cart',
        username=username
    )


# =========================================================
# RAZORPAY CREATE ORDER
# =========================================================

def create_razorpay_order(
    request,
    username
):

    if request.method != 'POST':

        return JsonResponse(
            {
                'error':
                    'Invalid request'
            },
            status=400
        )

    cart_items = Cart.objects.filter(
        username=username
    )

    if not cart_items.exists():

        return JsonResponse(
            {
                'error':
                    'Cart is empty'
            },
            status=400
        )

    total = 0

    for cart_item in cart_items:

        total = total + (
            cart_item.menu.price
            * cart_item.quantity
        )

    amount_in_paise = int(
        total * 100
    )

    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        )
    )

    razorpay_order = client.order.create(
        {
            'amount':
                amount_in_paise,

            'currency':
                'INR',

            'payment_capture':
                1
        }
    )

    return JsonResponse(
        {
            'key_id':
                settings.RAZORPAY_KEY_ID,

            'order_id':
                razorpay_order['id'],

            'amount':
                amount_in_paise,

            'currency':
                'INR'
        }
    )


# =========================================================
# RAZORPAY UPI QR CODE
# =========================================================

# =========================================================
# RAZORPAY UPI QR CODE
# =========================================================

def create_upi_qr(request, username):

    if request.method != 'POST':
        return JsonResponse(
            {'error': 'Invalid request'},
            status=400
        )

    cart_items = Cart.objects.filter(
        username=username
    )

    if not cart_items.exists():
        return JsonResponse(
            {'error': 'Cart is empty'},
            status=400
        )

    total = 0

    for cart_item in cart_items:
        total = total + (
            cart_item.menu.price
            * cart_item.quantity
        )

    amount_in_paise = int(total * 100)

    try:

        client = razorpay.Client(
            auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET
            )
        )

        # IMPORTANT:
        # Razorpay Python SDK uses qrcode.create()

        qr_code = client.qrcode.create(
            {
                'type': 'upi_qr',
                'name': 'Meal Mate',
                'usage': 'single_use',
                'fixed_amount': True,
                'payment_amount': amount_in_paise,
                'description': 'Meal Mate Food Order'
            }
        )

        return JsonResponse(
            {
                'qr_id': qr_code['id'],
                'image_url': qr_code['image_url'],
                'amount': amount_in_paise,
                'currency': 'INR'
            }
        )

    except Exception as error:

        print(
            "UPI QR creation error:",
            error
        )

        return JsonResponse(
            {
                'error':
                    'Unable to create UPI QR code.'
            },
            status=500
        )

# =========================================================
# CHECKOUT
# =========================================================

def checkout(
    request,
    username
):

    cart_items = Cart.objects.filter(
        username=username
    )

    if not cart_items.exists():

        return redirect(
            'cart',
            username=username
        )

    try:

        customer = Customer.objects.get(
            username=username
        )

    except Customer.DoesNotExist:

        return redirect(
            'open_signin'
        )

    menuList = []

    total = 0

    for cart_item in cart_items:

        item_total = (
            cart_item.menu.price
            * cart_item.quantity
        )

        total = total + item_total

        menuList.append(
            {
                'menu':
                    cart_item.menu,

                'quantity':
                    cart_item.quantity,

                'item_total':
                    item_total
            }
        )

    return render(
        request,
        'delivery/checkout.html',
        {
            'username':
                username,

            'customer':
                customer,

            'menuList':
                menuList,

            'total':
                total
        }
    )


# =========================================================
# PLACE ORDER
# =========================================================

def place_order(
    request,
    username
):

    if request.method != 'POST':

        return redirect(
            'checkout',
            username=username
        )

    cart_items = Cart.objects.filter(
        username=username
    )

    if not cart_items.exists():

        return redirect(
            'cart',
            username=username
        )

    try:

        customer = Customer.objects.get(
            username=username
        )

    except Customer.DoesNotExist:

        return redirect(
            'open_signin'
        )

    address = request.POST.get(
        'address'
    )

    mobile = request.POST.get(
        'mobile'
    )

    payment_method = request.POST.get(
        'payment_method',
        'cod'
    )

    total = 0

    for cart_item in cart_items:

        total = total + (
            cart_item.menu.price
            * cart_item.quantity
        )

    # =====================================================
    # RAZORPAY PAYMENT
    # =====================================================

    if payment_method == 'razorpay':

        razorpay_payment_id = request.POST.get(
            'razorpay_payment_id'
        )

        razorpay_order_id = request.POST.get(
            'razorpay_order_id'
        )

        razorpay_signature = request.POST.get(
            'razorpay_signature'
        )

        if not razorpay_payment_id:

            return HttpResponse(
                "Razorpay payment was not completed."
            )

        if not razorpay_order_id:

            return HttpResponse(
                "Razorpay order ID is missing."
            )

        if not razorpay_signature:

            return HttpResponse(
                "Razorpay payment signature is missing."
            )

        # =================================================
        # VERIFY RAZORPAY PAYMENT
        # =================================================

        try:

            client = razorpay.Client(
                auth=(
                    settings.RAZORPAY_KEY_ID,
                    settings.RAZORPAY_KEY_SECRET
                )
            )

            client.utility.verify_payment_signature(
                {
                    'razorpay_order_id':
                        razorpay_order_id,

                    'razorpay_payment_id':
                        razorpay_payment_id,

                    'razorpay_signature':
                        razorpay_signature
                }
            )

        except Exception as error:

            print(
                "Razorpay verification error:",
                error
            )

            return HttpResponse(
                "Razorpay payment verification failed."
            )

        # =================================================
        # CREATE PAID ORDER
        # =================================================

        order = Order.objects.create(

            username=username,

            mobile=mobile,

            address=address,

            total_amount=total,

            payment_method='Razorpay',

            razorpay_order_id=
                razorpay_order_id,

            razorpay_payment_id=
                razorpay_payment_id,

            status='Paid'
        )

    # =====================================================
    # CASH ON DELIVERY
    # =====================================================

    else:

        order = Order.objects.create(

            username=username,

            mobile=mobile,

            address=address,

            total_amount=total,

            payment_method='Cash on Delivery',

            status='Pending'
        )

    # =====================================================
    # CREATE ORDER ITEMS
    # =====================================================

    for cart_item in cart_items:

        OrderItem.objects.create(

            order=order,

            menu=cart_item.menu,

            quantity=cart_item.quantity,

            price=cart_item.menu.price
        )

    # =====================================================
    # CLEAR CART
    # =====================================================

    cart_items.delete()

    # =====================================================
    # ORDER SUCCESS
    # =====================================================

    return render(

        request,

        'delivery/order_success.html',

        {
            'order':
                order,

            'username':
                username
        }
    )

# =========================================================
# ORDER HISTORY
# =========================================================

def order_history(request, username):

    orders = Order.objects.filter(
        username=username
    ).order_by('-created_at')

    return render(
        request,
        'delivery/order_history.html',
        {
            'username': username,
            'orders': orders
        }
    )