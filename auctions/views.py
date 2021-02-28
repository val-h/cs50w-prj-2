from typing import List
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.utils import OperationalError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Category, Listing, User
from .forms import BidForm, ListingForm

def index(request):
    listings = Listing.objects.all()
    return render(request, 'auctions/index.html', {
        'listings': listings,
    })
    # try:
    #     listings = Listing.objects.all()
    # except OperationalError:
    #     return render(request, 'auctions/index.html', {
    #         'message': 'No listings available!',
    #     })
    # finally: 
    #     return render(request, "auctions/index.html", {
    #         'listings': listings,
    #     })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect('auctions:index')
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    return redirect('auctions:index')

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
        return redirect('auctions:index')
    else:
        return render(request, "auctions/register.html")

# My views
@login_required
def create_listing(request):
    if request.method == 'POST':
        # Never forget the request.FILES...
        # source: https://djangocentral.com/uploading-images-with-django/
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            new_listing = form.save(commit=False)
            new_listing.owner = request.user
            new_listing.save()
            return redirect('auctions:index')
        else:
            return render(request, 'auctions/create_listing.html', {
                'form': form,
            })
    else:
        form = ListingForm()
        return render(request, 'auctions/create_listing.html', {
            'form': form,
        })

def listing_view(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    return render(request, 'auctions/listing.html', {
        # Doesnt't save/load the image file corectly
        # look for how i set up the images on the blog app
        'listing': listing,
        'bid_form': BidForm(),
    })

@login_required
def watchlist_view(request):
    watchlist = None # To get current watchlist for a user
    return render(request, 'auctions/watchlist.html', {
        'watchlist': watchlist,
    })

def categories_view(request):
    categories = Category.objects.all()
    return render(request, 'auctions/categories.html', {
        'categories': categories,
    })

def category_view(request, category_id):
    category = Category.objects.get(id=category_id)
    return render(request, 'auctions/category.html', {
        'category': category,
    })

def bid(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(id=listing_id)
        form = BidForm(request.POST)
        if form.is_valid():
            new_bid = form.save(commit=False)
            new_bid.listing = listing
            new_bid.bidder = request.user
            new_bid.save()
            # listing.set() required, look at the error
            return redirect('auctions:listing', listing_id)
