from typing import List
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import IntegerField

# from django.utils.timezone import now as date_now


class User(AbstractUser):
    # date_created = models.DateTimeField(auto_now_add=True, default=date_now())
    
    # To be able to set from 'My Account' page, it will replace Watchlist
    # and be a combination of many features, settings(i guess), pfp, watchlist
    # current listings(owner's), current bids, comments etc.
    pfp = models.ImageField(blank = True)
    status = models.TextField(blank=True)
    # max and min rating to be added
    rating = models.IntegerField(blank=True)

class Category(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField()

    # See how to implement it with a function
    number_of_listings = IntegerField()

    def __str__(self) -> str:
        return f"{self.title}"

class Listing(models.Model):
    title = models.CharField(max_length=80)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    # Highly unlikely to delete Categories, unless i allow users to 
    # create categories but just in case, if category is deleted, the 
    # listing will survive.
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    # Optional
    image = models.ImageField(blank=True)

    def __str__(self) -> str:
        return f"{self.title}, created by: {self.owner}"

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="item")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f"Bid on: {self.listing}, by : {self.bidder}"

class Comment(models.Model):
    # Deleting the comment on User deletion may be optional
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentor")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing")
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self) -> str:
        return f"Comment on: {self.listing}, posted by: {self.owner}"
