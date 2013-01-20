# -*- coding: utf-8 -*-
import re

from django import forms
from django.core.validators import RegexValidator

from artexer.app.models import Page

slug_re = re.compile(r'^[a-z0-9_]+$')
validate_slug = RegexValidator(slug_re,
                               u'Введите правильный адрес из строчных'
                               u' английских букв, чисел и подчеркивания',
                              'invalid')

class SlugField(forms.CharField):
    default_error_messages = {
        'invalid': u'Введите правильный адрес из строчных'
                   u' английских букв, чисел и подчеркивания',
    }
    default_validators = [validate_slug]

    def validate(self, value):
        super(SlugField, self).validate(value)

        if value in ['admin', 'add', 'edit', 'delete']:
            raise forms.ValidationError(u'Значение %s зарезервирована'
                                        u' для внутреннего иcпользования.'
                                        u' Используйте другое значение' % value)


class PageAddForm(forms.ModelForm):

    slug = SlugField(label=u'Адрес')

    class Meta:
        model = Page
        fields = ('title', 'slug', 'text')

    def clean_slug(self):
        data = self.cleaned_data
        slug = data['slug']
        if Page.objects.filter(slug=slug).exists():
            raise forms.ValidationError(u"Страница с адресом %s"
                                        u" уже существует" % slug)

        return data

class PageEditForm(forms.ModelForm):

    class Meta:
        model = Page
        fields = ('title', 'text')
