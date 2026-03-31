"""View functions handling HTTP requests/responses.

Views receive HttpRequest from URL dispatcher, process with models/forms, return
HttpResponse (render, redirect, etc). Always check request.user.is_authenticated
for protected views - use @login_required decorator. Use get_object_or_404() to
raise 404 if object missing instead of catching exceptions. Follow: validate input,
process logic, return response.
"""
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from . import forms
from django.contrib import messages

from .models import User
from .models import Auction_Listing, Bid

Bid_Category = { "FR": "Fashion",
                 "TY": "Toys",
                 "AR": "Artifact",
                 "JW": "Jewelry",
                 "MC": "Machinary"}

def index(request):
    # .objects.all() -> gets me everything
    all_listings = Auction_Listing.objects.all()
    return render(request, "auctions/index.html",{
        "all_listings": all_listings,
        # Excludes all listings not watchlisted by the user
        "count_watchlist" : len(list(Auction_Listing.objects.exclude(watch=False)))
        # TODO -> Integrate user with this to have different user with different watchlists
    })

# TODO -> Implement a new tab for all of the listings created by the user.

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
        form = forms.CreateListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit = False) # Commit = False
            # commit = False, creates the instance of class (obj) 
            # but the data isn't written into the db yet -> waiting for some final edits
            listing.user = request.user
            # Like attaching the user who made the listing in the first place
            listing.bid_count = 0
            # Setting the bid_count = 0, 
            # which we will increment everytime someone places a higher bid
            listing.save()
            # This is saving the form, not the Auction_listing class though

            initial_bid = form.cleaned_data['starting_bid']
            
            return redirect('index')
    else:
        form = Auction_Listing()
    return render(request, "auctions/create.html", {
        "form" : form # If form isn't valid -> Direct to the same fields to edit
    })


# TODO -> Fix the size of the image in item.html (id -> bid_image)
def view_listing(request, listing_id):
    if request.method == "POST":
        # Search all listings with the listing_id
        listing = get_object_or_404(Auction_Listing, pk=listing_id)
        return render(request,"auctions/item.html",{
            "listing": listing
        })
    return redirect('index')

def watch(request,listing_id):
    if request.method == "POST":
        # First get the object via the pk id to toggle watch
        listing = get_object_or_404(Auction_Listing, pk=listing_id)

        # MANY TO MANY RELATIONSHIPS
            # The fields are not directly assigned values, 
            # instead they have sets, we can add or remove people from

        # Negation of watch field
        if request.user in listing.watch.all():
            listing.watch.remove(request.user)
        else:
            listing.watch.add(request.user)
        listing.save()
        # listing.save(update_fields=['watch'])
    # all_listings = Auction_Listing.objects.exclude()

    # To get some specific objects, like the users watchlist -> use .filter()
    # NOTE -> .exclude() does not work the same was as .filter() 
    all_listings = Auction_Listing.objects.filter(watch=request.user)

    # all_listings = Auction_Listing.objects.exclude(watch=False, user != user_id)
    
    return render(request, "auctions/watchlist.html",{
        "listings" : all_listings
    })

def watchlist(request):   
    all_listings = Auction_Listing.objects.exclude(watch=False)
    # all_listings = Auction_Listing.objects.exclude(watch=False, user != user_id)
    return render(request,"auctions/watchlist.html",{
        "listings": all_listings    
    })

def count_watchlist(request): # TODO
    # all_listings = Auction_Listings.objects.exclude(watch = False, user != user_id)
    pass
    
def new_bid(request, listing_id):
    # fetch the bid:
    form = get_object_or_404(Auction_Listing, pk=listing_id)
    new_bid_value = float(request.POST["new_bid"])
    if new_bid_value > form.new_bid:
        form.bid = new_bid_value
        form.bid_count += 1 # Here we increment the 
        form.save()
        # messages = "Bid placed sucessfully!"
        message = "Bid placed successfully!"
    else:
        message = "Bid must be higher than current price."
        
    
    return render(request, "auctions/item.html",{
        "listing": form,
        "new_bid_placed" : message
    })

    


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




