from django import forms
from .models import User_Webtoon

# Model Form (모델 폼)
class User_WebtoonForm(forms.ModelForm):
    class Meta:
        model = User_Webtoon
        fields = ['rating', 'review']
        labels = {
            'rating': '평점',
            'review': '리뷰',
        }
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 0, 'max': 10, 'step': 0.5}),
            'review': forms.Textarea(attrs={'rows': 5}),
        }