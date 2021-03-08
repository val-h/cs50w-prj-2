from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.utils import OperationalError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Category, Listing, User, Watchlist
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
            new_listing.current_price = request.POST['start_price']
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
    bids = listing.bids.all()
    total_bids = len(bids)
    return render(request, 'auctions/listing.html', {
        # Doesnt't save/load the image file corectly
        # look for how i set up the images on the blog app
        'listing': listing,
        'bids': bids,
        'total_bids': total_bids,
        'bid_form': BidForm(crnt_b=None),
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

# Didnt work as expected -> keeping it just for proof of work
#  Finally worked ;d
def check_user_bid_on_listing(listing, user, amount):
    # Make a querry set and take the first(and only) result
    current_bid = listing.bids.filter(bidder=user)[0]
    if current_bid and current_bid.amount < amount:
        return True
    elif current_bid.amount >= amount:
        return False
    # If the user doesn't have a bid at all
    return True
    #     if bid.bidder == user:
    #         if bid.amount > amount:
    #             return True
    #         elif bid.amount <= amount:
    #             return False
    # return True

    # if user.bids:
    #     # u_bid = [u_bid for u_bid in user.bids if u_bid.listing.id == listing.id]
    #     u_bid = user.bids
    #     print(u_bid)
    #     if u_bid and u_bid > amount:
    #         return True
    #     elif u_bid <= amount:
    #         return False
    #     return True
    # return True

# For the record, I spent another 5 hours just to figure out the validation
# for this form -> max 1 bid per user and comparing the bids.

@login_required
def bid(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(id=listing_id)
        bidder = request.user
        # Take the first (and only) result for the user's bid
        try:
            current_bid = listing.bids.filter(bidder=bidder)[0]
        except:
            current_bid = None

        form = BidForm(request.POST, crnt_b=current_bid)
        if form.is_valid():
            new_bid = form.save(commit=False)
            new_bid.listing = listing
            new_bid.bidder = bidder
            new_bid.save()
            return redirect('auctions:listing', listing_id)
        else:
            bids = listing.bids.all()
            total_bids = len(bids)
            return render(request, 'auctions/listing.html', {
                'listing': listing,
                'bids': bids,
                'total_bids': total_bids,    
                'bid_form': form,
            })
        
        # if check_user_bid_on_listing(listing, bidder, int(request.POST['amount'])):
        # else:
        #     pass
        #     # send error for form amount

@login_required
def comment(request, listing_id):
    pass

@login_required
def watchlist_view(request):
    # By far not the most effective method(don't know if it even works)
    # I will make watchlists from the admin app until i implement a proper 
    # watchlist for the user on init -> creation
    if not request.user.watchlist.all()[0]:
        new_watchlist = Watchlist(user=request.user)
        new_watchlist.save()
    watchlist = request.user.watchlist.get(id=1) # To get current watchlist for a user
    print(watchlist)
    print(watchlist, ' - test')
    return render(request, 'auctions/watchlist.html', {
        'listings': watchlist.listings.all(),
    })
    
# Finish the watchlist feature
# figure out the manytomany realtions

# FINALLY WORKED!!!
# Still really bad implementation but it worked!
@login_required
def add_to_watchlist(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    user = request.user
    watchlist = user.watchlist.all()[0]
    # If the user doesn't have a watchlist, create it
    if not user.watchlist:
        new_watchlist = Watchlist(user=user)
        new_watchlist.save()
    print('test', user.watchlist)
    watchlist.listings.add(listing)
    return redirect('auctions:listing', listing_id)
