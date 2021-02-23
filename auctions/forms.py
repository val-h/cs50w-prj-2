from django import forms
from django.forms import fields

from .models import *

# Sample, try using model forms

class ListingForm(forms.ModelForm):
    # title = models.CharField(max_length=120)
    # description = models.TextField()
    class Meta:
        model = Listing
        fields = [
        'title',
        'description',
        'category',
        'image',]
        labels = {}

# TODO
class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = []
        pass

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = []
        pass

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = []
        pass
