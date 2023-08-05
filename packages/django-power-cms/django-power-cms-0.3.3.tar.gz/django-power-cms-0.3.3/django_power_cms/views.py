from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .models import Page
from .models import Site
from django.contrib.auth.models import User

def site(request, site_code):
    site = get_object_or_404(Site, published=True, code=site_code)
    if site.index_page_code:
        url = reverse("django-power-cms.page", kwargs={"site_code": site.code, "page_code": site.index_page_code})
        return HttpResponseRedirect(url)
    else:
        raise Http404()

def page(request, site_code, page_code):
    page = get_object_or_404(Page,site__code=site_code, code=page_code)
    if not page.is_published:
        raise Http404()
    context = {
        "request": request,
        "site_code": site_code,
        "page_code": page_code,
        "site": page.site,
        "page": page,
        "title": page.site.name + " | " + page.name
    }
    html = page.render(request, context)
    return HttpResponse(html)

