from django import forms
from django.core.exceptions import ValidationError
from django.forms import fields
from django.http import request
from django.utils.translation import gettext as _
from django.conf import settings

from PIL import Image

from .models import *

# Sample, try using model forms

class ListingForm(forms.ModelForm):

    # I spent 1 hour to make this validation, just to realise django wasn't built
    # with support for the Image class from PIL :))))) , best time in my life. 

    # I spent waaaay too much time on this validation that i should have!
    # sources: 
    # https://stackoverflow.com/questions/6195478/max-image-size-on-file-upload
    # https://pillow.readthedocs.io/en/latest/handbook/tutorial.html
    # Tho i had my own spin on the solution
    
    # def clean_image(self, max_size=settings.MAX_IMAGE_SIZE):
    #     # Open the image without loading it into memory
    #     # image = Image.open(self.cleaned_data.get('image'), mode='r')
    #     # if image:
    #     #     if image.format not in settings.ALLOWED_IMAGE_FORMATS:
    #     #         if image.size[0] * image.size[1] > max_size * 1024 * 1024:
    #     #             raise forms.ValidationError(f'Image size too big, maximum size is {max_size}MB.')
    #     #         return image
    #     #     else:
    #     #         raise forms.ValidationError(f'Image format {image.format} is not supported! Try a common one.')
    #     # else:
    #     #     raise forms.ValidationError('Couldn\'t upload the image.')

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
        # else:
        #     raise forms.ValidationError('Couldn\'t upload the image.')

        # i can't belive it works, i am probably missing something, oh w/e
        # write me a message in github if you think this has a problem or it is one big problem.

        # Fun fact, i didn't even have to implement the validation nor the image upload feature 
        # at all but i started it and i had to finish it!

    class Meta:
        model = Listing
        fields = [
        'title',
        'category',
        'start_price',
        'description',
        'image',]

# TODO
class BidForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.current_bid = kwargs.pop('crnt_b')
        self.listing = kwargs.pop('l')
        super(BidForm, self).__init__(*args, **kwargs)

    # Trying to check if the user already has a bid and if the price is lower than the current one
    def clean_amount(self):
        requested_bid_price = self.cleaned_data.get('amount')
        # print(requested_bid_price, type(requested_bid_price))
        if self.current_bid and self.current_bid.amount >= requested_bid_price:
            raise forms.ValidationError(_(f'The amount must be higher than your current bid: {self.current_bid.amount}.'), code='invalid')        
        elif requested_bid_price <= self.listing.current_price:
            raise forms.ValidationError(_(f'The amount must be higher than the current price: {self.listing.current_price}.'), code='invalid')
        return requested_bid_price

        # I really don't know what im doing here anymore
        # look into https://stackoverflow.com/questions/53955850/pass-variable-from-view-to-form-django
        # these 2 variables are none since cleaned_data doesn't have them ;d

    class Meta:
        model = Bid
        fields = [
            'amount',
        ]

# i wanted to make so users can add cattegories and i will finish this!
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'title',
            'description',
        ]
        pass

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'content',
        ]
        pass
