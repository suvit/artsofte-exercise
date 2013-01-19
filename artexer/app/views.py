# Create your views here.
from django.template.response import TemplateResponse
from artexer.app.models import Page

def home(request):
    pages = Page.objects.all()
    return TemplateResponse(request,
                            'base.html',
                            {'pages':pages}
                           )

def page_add(request, page1=None):
    pass

def page_view(request, page1, page2=None):
    pass

def page_edit(request, page1, page2=None):
    pass

def page_delete(request, page1, page2=None):
    pass

