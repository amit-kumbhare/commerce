from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    pass
class Auction_Listing(models.Model):
    title = models.TextField(max_length=64)
    description = models.TextField(max_length=200, blank=True)
    bid = models.DecimalField(decimal_places=2, max_digits=6)
    # Now search how to make certain places optional
    # -> by making blank = True
    img = models.ImageField(blank=True)
    watch = models.BooleanField(blank=False)
    # Some Categories
    Bid_Category = { "FR": "Fashion",
                     "TY": "Toys",
                     "AR": "Artifact",
                     "JW": "Jewelry",
                     "MC": "Machinary"}
    # Add more when required
    category = models.CharField(max_length=2, choices=Bid_Category, blank=True)

class Bid(models.Model):
    # name = User()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bid")
    listing = models.ForeignKey(Auction_Listing, on_delete=models.CASCADE, related_name="bids")
    current_bid = models.DecimalField(decimal_places=2, max_digits=6)
    time = models.DateTimeField(auto_now_add=True) # Adds time of when created

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Auction_Listing, on_delete=models.CASCADE, related_name="listing_comments")
    text = models.TextField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)














































    
