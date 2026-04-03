"""Django forms for user input validation.

Defines ModelForms and Forms for server-side validation, CSRF protection, and
data cleaning. Django forms handle HTML rendering, error display, and sanitization.
Always use forms instead of manual validation - follows DRY principle and security
best practices.
"""
from django import forms
from . import models

Bid_Category = [ ("FR","Fashion"),("TY","Toys"), ("AR", "Artifact"),("JW", "Jewelry"),
                 ("MC","Machinary")]

# django -> forms.ChoiceField take list of Tuples
# ("Code","Human-readable-name")

# class CreateListingForm(forms.Form):
#     title = forms.CharField(label="Title", max_length=64)
#     description = forms.CharField(widget=forms.Textarea)


#     starting_bid = forms.DecimalField(max_digits=10, decimal_places=2)
#     img = forms.ImageField()
#     category = forms.ChoiceField(choices=Bid_Category)

# Form to bridge between model and database
"""
class class-name(forms.ModelForm):

    # Here comes OVERRIDDEN FIELDS
    Which we want to override over the models field
    EG -> field says text input -> which html for uses <input type="text">
    we want description in textarea -> So we override it

    class Meta:
        model = model-name
        fields = ['required-field1','required-field2']

"""

class CreateListingForm(forms.ModelForm):
    # BUG -> title html uses textarea
    title = forms.CharField(widget=forms.TextInput)
    class Meta:
        model = models.Auction_Listing
        fields = ["title", "description","starting_bid","img","category"]

class CreateComment(forms.ModelForm):
    text = forms.CharField(widget=forms.TextInput)
    class Meta:
        model = models.Comment
        fields = ["text"]
