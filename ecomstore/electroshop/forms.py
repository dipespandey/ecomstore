from .models import Product,Category,UserProfile, CartItem
from django import forms
from django.contrib.auth.models import User

#normal form that is same as the django User
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username','email','password')


# a modified form with additional profile pic to the django User
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)


# form to add a cart to the user
class AddtoCartForm(forms.ModelForm):
	class Meta:
		model = CartItem
		fields = ('quantity',)


# form to deliver the product to the required address
class DeliverProductForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('delivery_address','phone',)

