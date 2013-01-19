# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

class Page(models.Model):
    title = models.CharField(u'Заголовок', max_length=300)
    slug = models.SlugField(u'Адрес')
    text = models.TextField(u'Текст')
    parent = models.ForeignKey('self', verbose_name=u'Родитель')

    class Meta:
        pass
