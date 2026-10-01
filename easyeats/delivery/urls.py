from django.urls import path
from . import views


urlpatterns = [

    # ================= HOME =================

    path(
        '',
        views.index,
        name='index'
    ),

    path(
        'about/',
        views.about,
        name='about'
    ),

    path(
        'contact/',
        views.contact,
        name='contact'
    ),

    path(
        'logout/',
        views.logout,
        name='logout'
    ),


    # ================= SIGN UP / SIGN IN =================

    path(
        'open_signup/',
        views.open_signup,
        name='open_signup'
    ),

    path(
        'open_signin/',
        views.open_signin,
        name='open_signin'
    ),

    path(
        'signup',
        views.signup,
        name='signup'
    ),

    path(
        'signin',
        views.signin,
        name='signin'
    ),


    # ================= ADMIN - RESTAURANT =================

    path(
        'open_add_restaurant',
        views.open_add_restaurant,
        name='open_add_restaurant'
    ),

    path(
        'add_restaurant',
        views.add_restaurant,
        name='add_restaurant'
    ),

    path(
        'open_show_restaurant',
        views.open_show_restaurant,
        name='open_show_restaurant'
    ),

    path(
        'open_update_restaurant/<int:restaurant_id>',
        views.open_update_restaurant,
        name='open_update_restaurant'
    ),

    path(
        'update_restaurant/<int:restaurant_id>',
        views.update_restaurant,
        name='update_restaurant'
    ),

    path(
        'delete_restaurant/<int:restaurant_id>',
        views.delete_restaurant,
        name='delete_restaurant'
    ),


    # ================= ADMIN - MENU =================

    path(
        'open_update_menu/<int:restaurant_id>',
        views.open_update_menu,
        name='open_update_menu'
    ),

    path(
        'delete_menu/<int:menu_id>',
        views.delete_menu,
        name='delete_menu'
    ),


    # ================= CUSTOMER - VIEW MENU =================

    path(
        'view_menu/<int:restaurant_id>/<str:username>',
        views.view_menu,
        name='view_menu'
    ),


    # ================= ADD TO CART =================

    path(
        'add_to_cart/<int:menu_id>/<int:restaurant_id>/<str:username>',
        views.add_to_cart,
        name='add_to_cart'
    ),


    # ================= CART =================

    path(
        'cart/<str:username>',
        views.cart,
        name='cart'
    ),


    # ================= REMOVE FROM CART =================

    path(
        'remove_from_cart/<int:menu_id>/<str:username>',
        views.remove_from_cart,
        name='remove_from_cart'
    ),


    # ================= INCREASE QUANTITY =================

    path(
        'increase_cart/<int:menu_id>/<str:username>',
        views.increase_cart,
        name='increase_cart'
    ),


    # ================= DECREASE QUANTITY =================

    path(
        'decrease_cart/<int:menu_id>/<str:username>',
        views.decrease_cart,
        name='decrease_cart'
    ),


    # ================= CHECKOUT =================

    path(
        'checkout/<str:username>',
        views.checkout,
        name='checkout'
    ),


    # ================= RAZORPAY =================

    path(
        'create_razorpay_order/<str:username>',
        views.create_razorpay_order,
        name='create_razorpay_order'
    ),

    path(
        'create_upi_qr/<str:username>',
        views.create_upi_qr,
        name='create_upi_qr'
    ),


    # ================= PLACE ORDER =================

    path(
        'place_order/<str:username>',
        views.place_order,
        name='place_order'
    ),

        # ================= ORDER HISTORY =================

    path(
        'order_history/<str:username>',
        views.order_history,
        name='order_history'
    ),

]