# -*- coding: utf-8 -*-
import re

from django import forms
from django.core.validators import RegexValidator

from pytils.translit import slugify

from artexer.app.models import Page

slug_re = re.compile(r'^[a-z0-9_]+$')
validate_slug = RegexValidator(slug_re,
                               code='invalid')

class SlugField(forms.CharField):
    default_error_messages = {
        'invalid': u'Введите правильный адрес из строчных'
                   u' английских букв, чисел и подчеркивания',
    }
    default_validators = [validate_slug]


class PageAddForm(forms.ModelForm):

    slug = SlugField(label=u'Адрес', required=False)

    class Meta:
        model = Page
        fields = ('title', 'slug', 'text', 'parent')
        widgets = {'parent': forms.HiddenInput}

    def clean_slug(self):
        slug = self.cleaned_data['slug']

        if slug == '' and 'title' in self.cleaned_data:
            slug = slugify(self.cleaned_data['title'])
            slug = slug.replace('-','_').lower()

        if slug in ['admin', 'add', 'edit', 'delete']:
            raise forms.ValidationError(u'Значение %s зарезервирована'
                                        u' для внутреннего иcпользования.'
                                        u' Используйте другое значение' % slug)

        return slug

class PageEditForm(forms.ModelForm):

    class Meta:
        model = Page
        fields = ('title', 'text')
