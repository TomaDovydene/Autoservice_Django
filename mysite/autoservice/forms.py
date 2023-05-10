from .models import OrderReview
from django import forms
from .models import Profile
from django.contrib.auth.models import User
from .models import Order

class OrderReviewForm(forms.ModelForm):
    class Meta:
        model = OrderReview
        fields = ('content',)
        widgets = {'order': forms.HiddenInput(), 'reviewer': forms.HiddenInput()}


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']


class DateInput(forms.DateInput):
    input_type = 'datetime-local'


class OrderCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['due_back', 'vehicle', 'status']
        widgets = {'due_back': DateInput()}
