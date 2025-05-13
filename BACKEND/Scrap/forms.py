from django import forms

class ScrapingForm(forms.Form):
    spider = forms.ChoiceField(label="Choisir le site à scraper")
    category = forms.CharField(required=False, label="Catégorie (optionnel)")
