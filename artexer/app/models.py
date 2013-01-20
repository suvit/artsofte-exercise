# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse

from django.db import models

# Create your models here.

class Page(models.Model):
    title = models.CharField(u'Заголовок', max_length=300)
    slug = models.SlugField(u'Адрес')
    text = models.TextField(u'Текст')
    parent = models.ForeignKey('self', verbose_name=u'Родитель',
                               blank=True, null=True)

    class Meta:
        unique_together = ('parent', 'slug')

    def __unicode__(self):
        try:
            url = self.get_absolute_url()
        except:
            url = '/'
        return u'%s (%s)' % (self.title, url)

    def clean(self):
        if not self.parent and Page.objects.filter(slug=self.slug).exists():
            raise ValidationError(u"Адрес %s уже существует. Используйте другой адрес" % self.slug)

    def get_absolute_url(self):
        args = [ self.slug ]
        self.parent_id and args.insert(0, self.parent.slug)
        return reverse('page_view', args=args)

    def get_text(self):
        return self.text

    def get_children(self):
        return Page.objects.filter(parent=self)
