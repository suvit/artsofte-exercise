from django import forms

from artexer.app.models import Page

class PageAddForm(forms.ModelForm):
    model = Page

    class Meta:
        fields = ('title', 'slug', 'text')

class PageEditForm(forms.ModelForm):
    model = Page

    class Meta:
        fields = ('title', 'text')
