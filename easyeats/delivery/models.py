from django.db import models


# ================= CUSTOMER =================

class Customer(models.Model):

    username = models.CharField(max_length=20)

    password = models.CharField(max_length=20)

    email = models.CharField(max_length=20)

    mobile = models.CharField(max_length=10)

    address = models.CharField(max_length=50)

    def __str__(self):
        return self.username


# ================= RESTAURANT =================

class Restaurant(models.Model):

    name = models.CharField(max_length=20)

    picture = models.URLField(
        max_length=200,
        default='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSSdkMXTi0dr23JhKjdMHoWzGEmlPbcKxNA7fBXyEvKOU-xcdlu8iyrBcuX&s=10'
    )

    cuisine = models.CharField(max_length=200)

    rating = models.FloatField()

    def __str__(self):
        return self.name


# ================= MENU =================

class Menu(models.Model):

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE
    )

    food_name = models.CharField(max_length=100)

    picture = models.URLField(
        max_length=500,
        default=''
    )

    description = models.CharField(
        max_length=255
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    is_veg = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.food_name


# ================= CART =================

class Cart(models.Model):

    username = models.CharField(
        max_length=20
    )

    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE
    )

    quantity = models.IntegerField(
        default=1
    )

    def __str__(self):
        return self.username + " - " + self.menu.food_name


# ================= CONTACT MESSAGE =================

class ContactMessage(models.Model):

    name = models.CharField(max_length=100)

    email = models.EmailField()

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


# ================= ORDER =================

class Order(models.Model):

    username = models.CharField(max_length=20)

    mobile = models.CharField(
        max_length=10
    )

    address = models.CharField(
        max_length=255
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=30,
        default='Cash on Delivery'
    )

    razorpay_order_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    razorpay_payment_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=30,
        default='Pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return "Order #" + str(self.id) + " - " + self.username


# ================= ORDER ITEM =================

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE
    )

    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE
    )

    quantity = models.IntegerField(
        default=1
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return self.menu.food_name + " x " + str(self.quantity)