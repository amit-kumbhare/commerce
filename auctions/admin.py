from django.contrib import admin

# Register your models here.
from .models import AbstractUser
from .models import Auction_Listing
from .models import Bid
from .models import Comment

admin.site.register(Auction_Listing)
admin.site.register(Bid)
admin.site.register(Comment)