"""Django admin interface configuration.

Registers models for admin site management. Use admin.site.register() to expose
models in Django's built-in admin panel for CRUD operations. Only define here
what needs admin access - improves security by limiting exposure.
"""
from django.contrib import admin

# Register your models here.
from .models import AbstractUser
from .models import Auction_Listing
from .models import Bid
from .models import Comment

admin.site.register(Auction_Listing)
admin.site.register(Bid)
admin.site.register(Comment)