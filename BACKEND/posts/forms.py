from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Contenu'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Catégorie'}),
        }
