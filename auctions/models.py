from typing import List
# from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import IntegerField
from decimal import Decimal

# from django.utils.timezone import now as date_now


class User(AbstractUser):
    pass
    # date_created = models.DateTimeField(auto_now_add=True)
    
    # implemented at the end

    # To be able to set from 'My Account' page, it will replace Watchlist
    # and be a combination of many features, settings(i guess), pfp, watchlist
    # current listings(owner's), current bids, comments etc.

    # pfp = models.ImageField(upload_to='images/pfps', blank=True)
    # to be placed default -> auctions/static/images/default.jpg

    # status = models.CharField(max_length=20, blank=True)
    # max and min rating to be added
    # rating = models.IntegerField(blank=True)

class Category(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField()

    def __str__(self) -> str:
        return f"{self.title}"

class Listing(models.Model):
    title = models.CharField(max_length=80)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    date = models.DateTimeField(auto_now_add=True)
    start_price = models.DecimalField(max_digits=12, decimal_places=2)
    current_price = models.DecimalField(max_digits=12, decimal_places=2)
    watchlists = models.ManyToManyField(User, related_name='watchlist')

    # Optional
    image = models.ImageField(upload_to="images/", blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, blank=True)

    def __str__(self) -> str:
        return f"{self.title}, created by: {self.owner}"

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self) -> str:
        return f"Bid on: {self.listing}; bid by : {self.bidder}"

class Comment(models.Model):
    # Deleting the comment on User deletion may be optional
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self) -> str:
        return f"Comment on: {self.listing}; posted by: {self.owner}"
