from django import forms
from django.db import models

# Sample, try using model forms

class ListingForm(forms.Form):
    title = models.CharField(max_length=120)
    description = models.TextField()

