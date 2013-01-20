# Create your views here.
from django import http
from django.core.urlresolvers import reverse, resolve
from django.template import RequestContext, loader
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404, redirect

from artexer.app.forms import PageAddForm, PageEditForm
from artexer.app.models import Page


def get_page(page1, page2=None):
    kwargs = {'slug': page1}
    if page2 is not None:
        kwargs['parent__slug'] = page2
    else:
        kwargs['parent__isnull'] = True
    return get_object_or_404(Page, **kwargs)


def home(request):
    pages = Page.objects.all()
    return TemplateResponse(request,
                            'base.html',
                            {'pages': pages}
                           )


def page_add(request, page1=None, page2=None):
    parent = None
    initial = {}
    if page1 is page2 is None:
        # add parent page without name
        pass
    elif page2 is None:
        try:
            page = get_page(page1)
        except http.Http404:
            initial['slug'] = initial['title'] = page1
        else:
            # add to founded page
            parent = page
    else:
        try:
            page = get_page(page1, page2)
        except http.Http404:
            try:
                parent = get_page(page2)
            except http.Http404:
                return redirect('page_add', page2)
            else:
                initial['slug'] = initial['title'] = page1
        else:
            return redirect('page_edit', **{'page1': page1,
                                            'page2': page2})

    form = PageAddForm(request.POST or None, initial=initial)
    if request.method == 'POST':
        if form.is_valid():
            new_page = form.save(commit=False)
            if parent:
                new_page.parent = parent
            new_page.save()

            return redirect(new_page.get_absolute_url())

    return TemplateResponse(request,
                            'page/edit.html',
                            {'form': form,
                             'parent': parent}
                           )


def page_view(request, page1, page2=None):
    page = get_page(page1, page2)
    return TemplateResponse(request,
                            'page/view.html',
                            {'page': page},
                           )


def page_edit(request, page1, page2=None):
    page = get_page(page1, page2)

    form = PageEditForm(request.POST or None, instance=page)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(form.instance.get_absolute_url())

    return TemplateResponse(request,
                            'page/edit.html',
                            {'form': form}
                           )


def page_delete(request, page1, page2=None):
    page = get_page(page1, page2)
    if 'confirm' in request.GET:
        page.delete()
        return redirect('home')

    return TemplateResponse(request,
                            'page/delete.html',
                            {'page': page},
                           )


def page_404(request):
    vars_ = {'request_path': request.path}
    try:
        func, args, kwargs = resolve(request.path)
    except http.Http404:
        pass
    else:
        if func is page_view:
            vars_['page_add'] = reverse('page_add', kwargs=kwargs)
        elif func is page_edit:
            vars_['page_add'] = reverse('page_add', kwargs=kwargs)
        elif func is page_delete:
            vars_['page_add'] = reverse('page_add', kwargs=kwargs)

    context = RequestContext(request,
                             vars_
                             )

    t = loader.get_template('404.html')
    return http.HttpResponseNotFound(t.render(context))
