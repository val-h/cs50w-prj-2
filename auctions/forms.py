from django import forms
from django.core.exceptions import ValidationError
from django.forms import fields
from django.http import request
from django.utils.translation import gettext as _
from django.conf import settings

from PIL import Image

from .models import *

class ListingForm(forms.ModelForm):

    def clean_image(self, max_size=settings.MAX_IMAGE_SIZE):
        # source for this: https://docs.djangoproject.com/en/3.1/ref/forms/validation/
        image = self.cleaned_data.get('image')
        if image:

            # temp var just to test the file formats :D
            # not the most elegant or best way to do it but i wasted enough
            # time on these validations (learning them on the job)
            # Time spent: 2 hours   - will update if i get stuck again

            img_format = Image.open(image).format

            if img_format.lower() in settings.ALLOWED_IMAGE_FORMATS:
                # Check for the size
                if image.size > max_size * 1024 * 1024:
                    # This used to work, idk anymore
                    # raise forms.ValidationError({'images': f'Image size too big, maximum size is {max_size}MB.'}, code='invalid')
                    raise forms.ValidationError(_(f'Image size too big, maximum size is {max_size}MB.'), code='invalid')
                return image
            else:
                raise forms.ValidationError(_(f'Image format {img_format} is not supported! Try a common one.'), code='invalid')
        
    class Meta:
        model = Listing
        fields = [
        'title',
        'category',
        'start_price',
        'description',
        'image',]
        labels = {
            'title': '',
            'category': '',
            'start_price': '',
            'description': '',
            'image': '',
        }
        widgets = {
            'title': forms.TextInput(attrs = {'placeholder': 'Title'}),
            'description': forms.Textarea(attrs = {'placeholder': 'Description'}),
        }

# TODO
class BidForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.current_bid = kwargs.pop('crnt_b')
        self.listing = kwargs.pop('l')
        super(BidForm, self).__init__(*args, **kwargs)

    # Trying to check if the user already has a bid and if the price is lower than the current one
    def clean_amount(self):
        requested_bid_price = self.cleaned_data.get('amount')
        if self.current_bid and self.current_bid.amount >= requested_bid_price:
            raise forms.ValidationError(_(f'The amount must be higher than your current bid: {self.current_bid.amount}.'), code='invalid')        
        elif requested_bid_price <= self.listing.current_price:
            raise forms.ValidationError(_(f'The amount must be higher than the current price: {self.listing.current_price}.'), code='invalid')
        return requested_bid_price

    class Meta:
        model = Bid
        fields = [
            'amount',
        ]
        labels = {
            'amount': '',
        }

# i wanted to make so users can add cattegories and i will finish this!
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'title',
            'description',
        ]
        labels = {
            'title': '',
            'description': '',
        }
        widgets = {
            'title': forms.TextInput(attrs = {'placeholder': 'Title'}),
            'description': forms.TextInput(attrs = {'placeholder': 'Description'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'content',
        ]
        labels = {
            'content': '',
        }
