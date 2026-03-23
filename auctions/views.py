from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from . import forms

from .models import User
from .models import Auction_Listing

Bid_Category = { "FR": "Fashion",
                 "TY": "Toys",
                 "AR": "Artifact",
                 "JW": "Jewelry",
                 "MC": "Machinary"}

def index(request):
    all_listings = Auction_Listing.objects.all()
    return render(request, "auctions/index.html",{
        "all_listings": all_listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create(request):
    return render(request, "auctions/create.html",{
        "form": forms.CreateListingForm()
    })

def new_listing(request):
    if request.method == "POST":
        form = Auction_Listing(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = Auction_Listing()
    return render(request, "auctions/create.html", {
        "form" : form # If form isn't valid -> Direct to the same fields to edit
    })

def watch(request,listing_id):
    if request.method == "POST":
        # First get the object via the pk id to toggle watch
        listing = get_object_or_404(Auction_Listing, pk=listing_id)

        listing.watch = not listing.watch # Negation
        listing.save(update_fields=['watch'])
    return render(request, "auctions/watchlist.html")

def watchlist(request):
    # This would require all objs with tags 
    all_listings = Auction_Listing.objects.exclude(watch=False)
    # if not all_listings:
    #     return render(request,"auctions/watchlist.html",{
    #         "empty_watchlist": "Add something to you're Watchlist !"
    #     })
    # else:
    #     return render(request,"auctions/watchlist.html",{
    #         "listings":all_listings
    #     })
    
    all_listings = Auction_Listing.objects.exclude(watch=False)
    return render(request,"auctions/watchlist.html",{
        "listings": all_listings    })
    
def category(request):
    
    return render(request, "auctions/categories.html",{
        "all_listings" : Bid_Category.values()
    })

def category_search(request, category_id):
    all_listings = Auction_Listing.objects.filter(category=category_id)
    return render(request, "auctions/index.html",{
        "all_listings" : all_listings,
        "optional_text": f"All listings with Category as {category_id}"
    })


















































































