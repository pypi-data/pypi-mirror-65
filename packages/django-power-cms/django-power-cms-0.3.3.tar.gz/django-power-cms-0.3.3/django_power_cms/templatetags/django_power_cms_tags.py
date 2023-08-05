from django.template import Library
from ..models import Site
from ..models import Page

register = Library()


@register.filter
def smarturl(url):
    if not url:
        return "#"
    elif url.startswith("site:"):
        _, site_code = url.split(":")
        try:
            return Site.objects.get(code=site_code).get_absolute_url()
        except Site.DoesNotExist:
            return "#"
    elif url.startswith("page:"):
        _, site_code, page_code = url.split(":")
        try:
            return Page.objects.get(site__code=site_code, code=page_code).get_absolute_url()
        except Page.DoesNotExist:
            return "#"
    else:
        return url
