from .models import OrderReview
from django import forms

class OrderReviewForm(forms.ModelForm):
    class Meta:
        model = OrderReview
        fields = ('content',)
        widgets = {'order': forms.HiddenInput(), 'reviewer': forms.HiddenInput()}

