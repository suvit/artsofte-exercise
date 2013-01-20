import re
from itertools import cycle

from django import http
from django import template
from django.core.urlresolvers import reverse, resolve

from artexer.app.views import get_page, page_view

register = template.Library()

quot_re = re.compile('"|\'')
links_re = re.compile('\[{1,2}(?P<link>[^\s\]]+)(?P<name>[^\]]*)\]{1,2}')


@register.filter
def wiki_render(text):
    quote_cycle = cycle(['&laquo;', '&raquo;'])
    while True:
        try:
            part1, part2 = quot_re.split(text, 1)
        except ValueError:
            break
        text = quote_cycle.next().join((part1, part2))

    def link_finder(matchobj):
        classes = ''
        link = matchobj.group('link')

        if link.startswith('http') or link.startswith('https'):
            pass
        elif not link.startswith('/'):
            link = '/' + link

        name = matchobj.group('name')
        if not name:
            name = link

        try:
            func, args, kwargs = resolve(link)
        except http.Http404:
            pass
        else:
            if func is page_view:
                try:
                    get_page(kwargs['page1'], kwargs.get('page2'))
                except http.Http404:
                    classes = 'class="not_found"'
                    link = reverse('page_add', kwargs=kwargs)

        return '<a %s href="%s">%s</a>' % (classes,
                                           link.replace('/', '&#47;'),
                                           name)

    text = links_re.sub(link_finder, text)

    b_cycle = cycle(['<b>', '</b>'])
    while True:
        try:
            part1, part2 = text.split('**', 1)
        except ValueError:
            break
        text = b_cycle.next().join((part1, part2))

    i_cycle = cycle(['<i>', '</i>'])
    while True:
        try:
            part1, part2 = text.split('//', 1)
        except ValueError:
            break
        text = i_cycle.next().join((part1, part2))

    u_cycle = cycle(['<u>', '</u>'])
    while True:
        try:
            part1, part2 = text.split('__', 1)
        except ValueError:
            break
        text = u_cycle.next().join((part1, part2))

    return '<br />'.join(text.splitlines())
