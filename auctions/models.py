from typing import List
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import IntegerField


class User(AbstractUser):
    pass

class Category(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField()

    # For later
    number_of_listings = IntegerField()

    def __str__(self) -> str:
        return f"{self.title}"

class Listing(models.Model):
    title = models.CharField(max_length=80)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category)

    # Optional
    image = models.ImageField()

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
