from django.contrib import admin
from .models import Customer, Restaurant, ContactMessage

admin.site.register(Customer)
admin.site.register(Restaurant)
admin.site.register(ContactMessage)