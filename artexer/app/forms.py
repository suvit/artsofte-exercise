from django import forms

from artexer.app.models import Page

class PageAddForm(forms.ModelForm):
    model = Page

class PageEditForm(forms.ModelForm):
    model = Page

