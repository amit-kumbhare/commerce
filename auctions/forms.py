from django import forms

class CreateListingForm(forms.Form):
    title = forms.CharField(label="Title", max_length=64)
    description = forms.CharField(widget=forms.Textarea)
    starting_bid = forms.DecimalField(max_digits=10, decimal_places=2)
    img = forms.ImageField()


    
