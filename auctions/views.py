from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.utils import OperationalError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Category, Listing, User, Watchlist
from .forms import BidForm, ListingForm, CommentForm, CategoryForm

# Helper functions
# Create a watchlist for the user, helper function
def _get_watchlist(user):
    try:
        watchlist = user.watchlist.get(user=user)
    except:
        new_watchlist = Watchlist(user=user)
        new_watchlist.save()
        watchlist = user.watchlist.get(user=user)
    return watchlist


def index(request):
    # Show only active listings
    listings = Listing.objects.filter(active=True)
    return render(request, 'auctions/index.html', {
        'listings': listings,
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
            new_listing.winner = None
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
    user_watchlist = _get_watchlist(request.user).listings.all()
    comments = listing.comments.all()
    return render(request, 'auctions/listing.html', {
        # Doesnt't save/load the image file corectly
        # look for how i set up the images on the blog app
        'listing': listing,
        'bids': bids,
        'total_bids': total_bids,
        'user_watchlist': user_watchlist,
        'comments': comments,
        'bid_form': BidForm(crnt_b=None, l=listing),
        'comment_form': CommentForm(),
    })

# Working :D
@login_required
def close_auction(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    listing.active = False
    listing.save()
    return redirect('auctions:listing', listing_id)

@login_required
def reopen_auction(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    listing.active = True
    listing.save()
    return redirect('auctions:listing', listing_id)

def categories_view(request):
    categories = Category.objects.all()
    category_form = CategoryForm()
    return render(request, 'auctions/categories.html', {
        'categories': categories,
        'form': category_form,
    })

def category_view(request, category_id):
    category = Category.objects.get(id=category_id)
    return render(request, 'auctions/category.html', {
        'category': category,
        'listings': category.listings.all(),
    })

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            new_category = form.save()
            return redirect('auctions:category', new_category.id)

@login_required
def bid(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(id=listing_id)
        print(listing.bids.all())
        bidder = request.user
        # Take the first (and only) result for the user's bid
        try:
            current_bid = listing.bids.filter(bidder=bidder)[0]
            print(current_bid)
        except:
            current_bid = None

        form = BidForm(request.POST, crnt_b=current_bid, l=listing)
        if form.is_valid():
            # delete the current bid
            listing.bids.filter(bidder=bidder).delete() # listing.bids.remove(current_bid) doesnt work
            new_bid = form.save(commit=False)
            new_bid.listing = listing
            new_bid.bidder = bidder
            new_bid.save()
            listing.current_price = new_bid.amount # change the highest bid
            listing.winner = bidder # Make the new winner the highest bidder
            listing.save()
            print(current_bid)
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

@login_required
def watchlist_view(request):
    watchlist = _get_watchlist(request.user)
    return render(request, 'auctions/watchlist.html', {
        'listings': watchlist.listings.all(),
    })

@login_required
def add_to_watchlist(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    watchlist = _get_watchlist(request.user)
    watchlist.listings.add(listing)
    return redirect('auctions:listing', listing_id)

@login_required
def remove_from_watchlist(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    watchlist = _get_watchlist(request.user)
    watchlist.listings.remove(listing)
    return redirect('auctions:listing', listing_id)

@login_required
def comment(request, listing_id):
    if request.method == 'POST':
        listing = Listing.objects.get(id=listing_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            new_commnet = form.save(commit=False)
            new_commnet.owner = request.user
            new_commnet.listing = listing
            new_commnet.save()
            return redirect('auctions:listing', listing_id)
