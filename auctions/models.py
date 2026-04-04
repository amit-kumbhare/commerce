"""Database models defining data structure.

Defines ORM models - each class maps to database table. Use ForeignKey for
relationships (one-to-many), on_delete parameter required (CASCADE/PROTECT/SET_NULL).
Use related_name for reverse relationships. Django handles migrations automatically
when models change. Never modify generated migrations - create new ones.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


# TODO -> 
class User(AbstractUser):
    """Custom user model extending Django's AbstractUser.
    
    Always use custom user early in project for future extensibility.
    Django best practice: define AUTH_USER_MODEL in settings.py.
    """
    pass

class Auction_Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_owner")
    # owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_owner", null=True, blank=True)
    title = models.TextField(max_length=64)
    description = models.TextField(max_length=200, blank=True)
    starting_bid = models.DecimalField(decimal_places=2, max_digits=6)
    # null=True lets the database store nothing, blank=True lets the form be empty
    img = models.ImageField(upload_to="auctions/listing_photos/", blank=True)
    watch = models.ManyToManyField(User, blank=False,related_name="user_watchlist")
    # Some Categories
    Bid_Category = [ ("FR","Fashion"),("TY","Toys"), ("AR", "Artifact"),("JW", "Jewelry"),
                 ("MC","Machinary")]
    # Add more when required
    category = models.CharField(
        max_length=2, 
        choices=Bid_Category, 
        blank=False)
    bid_count = models.IntegerField(default=0)
    created_datetime = models.DateTimeField(auto_now_add=True, null=True)

class Bid(models.Model):
    # name = User()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bid")
    listing = models.ForeignKey(Auction_Listing, on_delete=models.CASCADE, related_name="bids")
    current_bid = models.DecimalField(decimal_places=2, max_digits=6)
    time = models.DateTimeField(auto_now_add=True) # Adds time of when created

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Auction_Listing, on_delete=models.CASCADE, related_name="listing_comments")
    text = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)














































    
