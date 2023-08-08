from django import forms
from core.models import ProductReview

class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Wirte review"}))
    
    class Meta:
        model = ProductReview
        fields = ['review','rating']