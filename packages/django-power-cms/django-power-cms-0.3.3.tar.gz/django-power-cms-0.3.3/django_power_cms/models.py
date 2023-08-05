import json
import logging
from fastutils import listutils
from django.db import models
from django.template.loader import render_to_string
from django.apps import apps
from django.utils.html import mark_safe
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from django_ckeditor_5.fields import CKEditor5Field
from ckeditor.fields import RichTextField
from django_msms_admin.models import DjangoMsmsModelAbstractBase
from django_middleware_global_request.middleware import get_request
from .settings import CURRENT_SIET_ID_SESSION_KEY


logger = logging.getLogger(__name__)

def admin_site_get_selected_site():
    request = get_request()
    if request:
        site_id = request.session.get(CURRENT_SIET_ID_SESSION_KEY, None)
        site = Site.objects.get(pk=site_id)
        return site
    return None

def limit_choices_to_selected_site():
    site = admin_site_get_selected_site()
    return {
        "site": site,
    }

def get_url(url_raw):
    if not url_raw:
        return "#"
    if url_raw.startswith("site:"):
        site_code = url_raw[5:]
        return reverse("django-power-cms.site", kwargs={"site_code": site_code})
    if url_raw.startswith("page:"):
        _, site_code, page_code = url_raw.split(":")
        return reverse("django-power-cms.page", kwargs={"site_code": site_code, "page_code": page_code})
    try:
        return reverse(url_raw)
    except:
        return url_raw

class Theme(models.Model):
    code = models.CharField(max_length=32, unique=True, verbose_name=_("Code"))
    name = models.CharField(max_length=64, verbose_name=_("Name"))
    app_label= models.CharField(max_length=64, null=True, blank=True, verbose_name=_("App Label"))
    app_verbose_name = models.CharField(max_length=64, null=True, blank=True, verbose_name=_("App Verbose Name"))
    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))
    preview_image = models.CharField(max_length=128, null=True, blank=True, verbose_name=_("Preview Image"))
    is_default = models.BooleanField(default=False, verbose_name=_("Is default theme"))

    class Meta:
        verbose_name = _("Theme")
        verbose_name_plural = _("Themes")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        result = super().save(*args, **kwargs)
        if self.is_default:
            for theme in Theme.objects.filter(is_default=True).exclude(pk=self.pk):
                theme.is_default = False
        return result

    @property
    def css(self):
        return [x.css for x in self.css_files.all()]

    @property
    def js(self):
        return [x.js for x in self.js_files.all()]

    @classmethod
    def get_default_theme(cls):
        return cls.objects.filter(is_default=True).all()[0]

    @classmethod
    def register(cls, config):
        try:
            cls._register(config)
        except Exception as error:
            logger.exception("Register Theme failed: {0}".format(str(config)))

    @classmethod
    def _register(cls, config):
        code = config["code"]
        try:
            instance = Theme.objects.get(code=code)
        except Theme.DoesNotExist:
            instance = Theme()
            instance.code = code
        instance.name = config["name"]
        instance.app_label = config["app_label"]
        instance.app_verbose_name = config["app_verbose_name"]
        instance.description = config["description"]
        instance.preview_image = config["preview_image"]
        instance.save()
        old_css = dict([(x.css, x) for x in instance.css_files.all()])
        old_js = dict([(x.js, x) for x in instance.js_files.all()])
        # css handler
        for css in config["css"]:
            if not css in old_css:
                css_instance = ThemeCss()
                css_instance.theme = instance
                css_instance.css = css
                css_instance.order = 0
                css_instance.save()
            else:
                del old_css[css]
        for css, css_instance in old_css.items():
            css_instance.delete()
        old_css = dict([(x.css, x) for x in instance.css_files.all()])
        index = 0
        for css in config["css"]:
            index += 1000
            if old_css[css].order != index:
                old_css[css].order = index
                old_css[css].save()
        # js handler
        for js in config["js"]:
            if not js in old_js:
                js_instance = ThemeCss()
                js_instance.theme = instance
                js_instance.js = js
                js_instance.order = 0
                js_instance.save()
            else:
                del old_js[js]
        for js, js_instance in old_js.items():
            js_instance.delete()
        old_js = dict([(x.js, x) for x in instance.js_files.all()])
        index = 0
        for js in config["js"]:
            index += 1000
            if old_js[js].order != index:
                old_js[js].order = index
                old_js[js].save()

class ThemeCss(models.Model):
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name="css_files", verbose_name=_("Theme"))
    css = models.CharField(max_length=128, verbose_name=_("CSS File"))
    order = models.IntegerField(verbose_name=_("Order"))

    class Meta:
        verbose_name = _("Theme CSS")
        verbose_name_plural = _("Theme CSSes")
        ordering = ["order"]

    def __str__(self):
        return str(self.pk)

class ThemeJs(models.Model):
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name="js_files", verbose_name=_("Theme"))
    js = models.CharField(max_length=128, verbose_name=_("JS File"))
    order = models.IntegerField(verbose_name=_("Order"))

    class Meta:
        verbose_name = _("Theme JS")
        verbose_name_plural = _("Theme JSes")
        ordering = ["order"]

    def __str__(self):
        return str(self.pk)

class Template(models.Model):
    code = models.CharField(max_length=32, unique=True, verbose_name=_("Code"))
    name = models.CharField(max_length=64, verbose_name=_("Name"))
    app_label= models.CharField(max_length=64, null=True, blank=True, verbose_name=_("App Label"))
    app_verbose_name = models.CharField(max_length=64, null=True, blank=True, verbose_name=_("App Verbose Name"))
    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))
    preview_image = models.CharField(max_length=128, null=True, blank=True, verbose_name=_("Preview Image"))
    template = models.CharField(max_length=128, verbose_name=_("Template File"))

    class Meta:
        verbose_name = _("Template")
        verbose_name_plural = _("Templates")

    def __str__(self):
        return self.name

    @classmethod
    def register(cls, config):
        try:
            cls._register(config)
        except Exception as error:
            logger.exception("Register Template failed: {0}".format(str(config)))

    @classmethod
    def _register(cls, config):
        code = config["code"]
        try:
            instance = Template.objects.get(code=code)
        except Template.DoesNotExist:
            instance = Template()
            instance.code = code
        instance.name = config["name"]
        instance.app_label = config["app_label"]
        instance.app_verbose_name = config["app_verbose_name"]
        instance.description = config["description"]
        instance.preview_image = config["preview_image"]
        instance.template = config["template"]
        instance.save()
        old_slots = dict([(x.code, x) for x in instance.slots.all()])
        for slot_config in config["slots"]:
            code = slot_config["code"]
            name = slot_config["name"]
            order = slot_config["order"]
            if not code in old_slots:
                slot_instance = TemplateSlot()
                slot_instance.template = instance
                slot_instance.code = code
                slot_instance.name = name
                slot_instance.order = order
                slot_instance.save()
            else:
                if old_slots[code].name != name:
                    old_slots[code].name = name
                    old_slots[code].save()
                del old_slots[code]
        for code, slot in old_slots.items():
            slot.delete()

class TemplateSlot(models.Model):
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name="slots", verbose_name=_("Template"))
    code = models.CharField(max_length=32, verbose_name=_("Code"))
    name = models.CharField(max_length=32, verbose_name=_("Name"))
    order = models.IntegerField(null=True, blank=True, verbose_name=_("Order"))

    class Meta:
        verbose_name = _("Template Slot")
        verbose_name = _("Template Slots")
        ordering = ["template", "order"]
        unique_together = [
            ("template", "code"),
        ]

    def __str__(self):
        return "{0}-{1}".format(self.template.name, self.name)

class Site(models.Model):
    name = models.CharField(max_length=64, verbose_name=_("Name"))
    code = models.CharField(max_length=64, unique=True, verbose_name=_("Code"))
    published = models.BooleanField(verbose_name=_("Published"))
    published_time = models.DateTimeField(null=True, blank=True, verbose_name=_("Published Time"))
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Theme"))
    index_page_code = models.CharField(max_length=64, null=True, blank=True, verbose_name=_("Index Page Code"))
    favicon = models.ImageField(upload_to="site/favicons/", null=True, blank=True, verbose_name=_("FavIcon"))

    class Meta:
        verbose_name = _("Site")
        verbose_name_plural = _("Sites")


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.published and (not self.published_time):
            self.published_time = timezone.now()
        if not self.published:
            self.published_time = None
        return super().save(*args, **kwargs)

    @property
    def is_published(self):
        return self.published

    def get_theme(self):
        if self.theme:
            return self.theme
        else:
            return Theme.get_default_theme()

    def get_absolute_url(self):
        return reverse("django-power-cms.site", kwargs={"site_code": self.code})

class Page(MPTTModel):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, default=admin_site_get_selected_site, related_name="pages", verbose_name=_("Site"))
    parent = TreeForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="children", limit_choices_to=limit_choices_to_selected_site, verbose_name=_("Parent Page"))
    name = models.CharField(max_length=64, verbose_name=_("Name"))
    code = models.CharField(max_length=64, verbose_name=("Code"))
    order = models.IntegerField(null=True, blank=True, verbose_name=_("Order"))
    published = models.NullBooleanField(verbose_name=_("Published"))
    published_time = models.DateTimeField(null=True, blank=True, verbose_name=_("Published Time"))
    template = models.ForeignKey(Template, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Template"))
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Theme"))

    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")
        unique_together = [
            ("site", "code"),
        ]
    
    class MPTTMeta:
        order_insertion_by = ['order']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.published and (not self.published_time):
            self.published_time = timezone.now()
        if not self.published:
            self.published_time = None
        return super().save(*args, **kwargs)

    @property
    def is_published(self):
        if self.published == True:
            return True
        if self.published == False:
            return False
        if self.parent:
            return self.parent.is_published
        else:
            return self.site.is_published

    def get_absolute_url(self):
        return reverse("django-power-cms.page", kwargs={"site_code": self.site.code, "page_code": self.code})

    def get_theme(self):
        if self.theme:
            return self.theme
        elif self.parent:
            return self.parent.get_theme()
        else:
            return self.site.get_theme()

    def render(self, request, global_context):
        css_links = []
        js_links = []
        # append theme resources
        theme = self.get_theme()
        for css in theme.css:
            listutils.append_new(css_links, css)
        for js in theme.js:
            listutils.append_new(js_links, js)
        # render widgets
        # and append widget resources
        widgets = {}
        for binding in self.widget_bindings.all():
            if not binding.slot: # if PageWidget NOT provide slot, just ignore it
                continue
            if not binding.slot.code in widgets:
                widgets[binding.slot.code] = []
            widgets[binding.slot.code].append(binding.widget.render(request, global_context))
            for css in binding.widget.get_real_model().css:
                listutils.append_new(css_links, css)
            for js in binding.widget.get_real_model().js:
                listutils.append_new(js_links, js)
        # make context
        context = {}
        context.update(global_context or {})
        context["widgets"] = widgets
        context["css_links"] = css_links
        context["js_links"] = js_links
        # render to string
        return render_to_string(self.template.template, context, request=request)

class PageWidget(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="widget_bindings", verbose_name=_("Page"))
    slot = models.ForeignKey(TemplateSlot, on_delete=models.SET_NULL, null=True, blank=True, related_name="+", verbose_name=_("Slot"))
    order = models.IntegerField(default=0, verbose_name=_("Order"))
    widget = models.ForeignKey("Widget", on_delete=models.CASCADE, limit_choices_to=limit_choices_to_selected_site, related_name="+", verbose_name=_("Widget"))

    class Meta:
        verbose_name = _("Page Widget Binding")
        verbose_name_plural = _("Page Widget Bindings")
        ordering = ["slot", "order"]

    def __str__(self):
        return str(self.pk)

class Widget(DjangoMsmsModelAbstractBase, models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True, blank=True, default=admin_site_get_selected_site, related_name="widgets",verbose_name=_("Site"))
    name = models.CharField(max_length=64, verbose_name=_("Name"))
    # widget box settings
    title = models.CharField(max_length=128, null=True, blank=True, verbose_name=_("Title"))
    widget_with_border = models.BooleanField(default=False, verbose_name=_("Widget With border"))
    widget_body_padding = models.CharField(max_length=16, default="10px", null=True, blank=True, verbose_name=_("Widget Body Pading"))
    widget_style = models.CharField(max_length=256, null=True, blank=True, verbose_name=_("Widget Style"))
    widget_header_style = models.CharField(max_length=256, null=True, blank=True, verbose_name=_("Widget Header Style"))
    widget_body_style = models.CharField(max_length=256, null=True, blank=True, verbose_name=_("Widget Body Style"))
    widget_footer_style = models.CharField(max_length=256, null=True, blank=True, verbose_name=_("Widget Footer Style"))
    widget_class = models.CharField(max_length=256, null=True, blank=True, verbose_name=_("Widget Class"))
    widget_header_class = models.CharField(max_length=256, null=True, blank=True, verbose_name=_("Widget Header Class"))
    widget_body_class = models.CharField(max_length=256, null=True, blank=True, verbose_name=_("Widget Body Class"))
    widget_footer_class = models.CharField(max_length=256, null=True, blank=True, verbose_name=_("Widget Footer Class"))

    css = []
    js = []

    class Meta:
        verbose_name = _("Widget")
        verbose_name_plural = _("Widgets")

    def __str__(self):
        return self.name

    def render(self, request, global_context):
        context = {}
        context.update(global_context or {})
        header, footer = self.widget_header_and_footer_render(request, global_context)
        real_widget_model = self.get_real_model()
        if real_widget_model:
            body = real_widget_model.objects.get(pk=self.pk).render(request, global_context)
            context.update({
                "pk": self.pk,
                "widget_with_border": self.widget_with_border,
                "widget_body_padding": self.widget_body_padding or "",
                "widget_style": self.widget_style or "",
                "widget_header_style": self.widget_header_style or "",
                "widget_body_style": self.widget_body_style or "",
                "widget_footer_style": self.widget_footer_style or "",
                "widget_class": self.widget_class or "",
                "widget_header_class": self.widget_header_class or "",
                "widget_body_class": self.widget_body_class or "",
                "widget_footer_class": self.widget_footer_class or "",
                "header": header.strip(),
                "body": body.strip(),
                "footer": footer.strip(),
            })
            return render_to_string("django-power-cms/widgets/power-widget.html", context)
        else:
            return ""

    def widget_header_and_footer_render(self, request, global_context):
        top_left_links = []
        top_right_links = []
        bottom_left_links = []
        bottom_right_links = []
        links = self.links.all()
        for link in links:
            if link.role == WidgetLink.TOP_LEFT:
                top_left_links.append(link)
            elif link.role == WidgetLink.TOP_RIGHT:
                top_right_links.append(link)
            elif link.role == WidgetLink.BOTTOM_LEFT:
                bottom_left_links.append(link)
            elif link.role == WidgetLink.BOTTOM_RIGHT:
                bottom_right_links.append(link)
        header_context = {}
        footer_context = {}
        header_context.update(global_context or {})
        footer_context.update(global_context or {})
        header_context.update({
            "title": self.title,
            "top_left_links": top_left_links,
            "top_right_links": top_right_links,
        })
        footer_context.update({
            "bottom_left_links": bottom_left_links,
            "bottom_right_links": bottom_right_links,
        })
        header = render_to_string("django-power-cms/widgets/power-widget-header.html", header_context)
        footer = render_to_string("django-power-cms/widgets/power-widget-footer.html", footer_context)
        return header, footer

class WidgetLink(models.Model):
    TOP_LEFT = 1
    TOP_RIGHT = 2
    BOTTOM_LEFT = 3
    BOTTOM_RIGHT = 4
    ROLES = [
        (TOP_LEFT, _("Top Left")),
        (TOP_RIGHT, _("Top Right")),
        (BOTTOM_LEFT, _("Bottom Left")),
        (BOTTOM_RIGHT, _("Bottom Right")),
    ]

    Widget = models.ForeignKey(Widget, on_delete=models.CASCADE, related_name="links", verbose_name=_("Widget"))
    role = models.IntegerField(choices=ROLES, verbose_name=_("Widget Link Role"))
    title = models.CharField(max_length=32, verbose_name=_("Title"))
    url_raw = models.CharField(max_length=128, verbose_name=_("Url"))
    icon = models.CharField(max_length=64, null=True, blank=True, verbose_name=_("Icon Class"))
    target = models.CharField(max_length=16, null=True, blank=True, verbose_name=_("Link Target"))

    class Meta:
        verbose_name = _("Widget Link")
        verbose_name_plural = _("Widget Links")

    def url(self):
        return get_url(self.url_raw)
    url.short_description = _("URL")

class StaticHtmlWidget(Widget):
    html = models.TextField(null=True, blank=True, verbose_name=_("HTML Code"))

    msms_category = _("Django Power Cms Default Widgets")
    msms_priority = 2000

    class Meta:
        verbose_name = _("Static HTML Widget")
        verbose_name_plural = _("Static HTML Widgets")

    def render(self, request, global_context):
        return self.html

class CarouselWidget(Widget):
    width = models.IntegerField(null=True, blank=True, verbose_name=_("Width"))
    height = models.IntegerField(null=True, blank=True, verbose_name=_("Height"))

    css = [
        "bootstrap/css/bootstrap.min.css",
        "django-power-cms/widgets/carousel/css/carousel.css",
    ]
    js = [
        "jquery3/jquery.js",
        "bootstrap/js/bootstrap.min.js",
    ]

    msms_category = _("Django Power Cms Default Widgets")
    msms_priority = 4000

    class Meta:
        verbose_name = _("Carousel Widget")
        verbose_name_plural = _("Carousel Widgets")

    def render(self, request, global_context):
        return render_to_string("django-power-cms/widgets/carousel.html", {
            "pk": self.pk,
            "images": self.images.all(),
            "width": self.width,
            "height": self.height,
        })

class CarouselWidgetImage(models.Model):
    carousel = models.ForeignKey(CarouselWidget, on_delete=models.CASCADE, related_name="images", verbose_name=_("Carousel"))
    image = models.ImageField(upload_to="carousel-images", verbose_name=_("Image"))
    url = models.CharField(max_length=512, null=True, blank=True, verbose_name=_("URL"))
    target = models.CharField(max_length=32, null=True, blank=True, verbose_name=_("URL Target"))
    order = models.IntegerField(default=0, verbose_name=_("Order"))

    class Meta:
        verbose_name = _("Carousel Widget Image")
        verbose_name_plural =  _("Carousel Widget Images")
        ordering = ["order"]

    def __str__(self):
        return str(self.pk)

class StaticListWidget(Widget):
    max_display_count = models.IntegerField(null=True, blank=True, verbose_name=_("Max Display Count"))
    empty_display_message = models.TextField(null=True, blank=True, verbose_name=_("Empty Display Message"))

    msms_category = _("Django Power Cms Default Widgets")
    msms_priority = 3000

    class Meta:
        verbose_name = _("Static List Widget")
        verbose_name_plural = _("Static List Widgets")

    def render(self, request, global_context):
        if self.max_display_count:
            lists = self.lists.filter(published=True).order_by("order").all()[:self.max_display_count]
        else:
            lists = self.lists.filter(published=True).order_by("order").all()
        return render_to_string("django-power-cms/widgets/static-list.html", {
            "lists": lists,
            "lists_length": len(lists),
            "empty_display_message": self.empty_display_message,
        })

class StaticListItem(models.Model):
    thelist = models.ForeignKey(StaticListWidget, on_delete=models.CASCADE, related_name="lists", verbose_name=_("The Static List Widget"))
    title = models.CharField(max_length=128, verbose_name=_("Title"))
    url = models.CharField(max_length=512, null=True, blank=True, verbose_name=_("URL"))
    target = models.CharField(max_length=32, null=True, blank=True, verbose_name=_("URL Target"))
    order = models.IntegerField(default=0, verbose_name=_("Order"))
    label = models.CharField(max_length=128, verbose_name=_("Label"))
    label_class = models.CharField(max_length=32, verbose_name=_("Label Class"))

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title

class TopbarWidget(Widget):
    welcome_message_for_login_user = models.CharField(max_length=128, null=True, blank=True, verbose_name=_("Welcome Message For Login User"))
    welcome_message_for_anonymous_user = models.CharField(max_length=128, null=True, blank=True, verbose_name=_("Welcome Message For Anonymous User"))
    fix_position = models.BooleanField(default=False, verbose_name=_("Fix Position"))
    show_login_or_logout_link = models.BooleanField(default=False, verbose_name=_("Show Login Or Logout Link"))
    login_link_raw = models.CharField(max_length=128, null=True, blank=True, verbose_name=_("Login Link"))
    logout_link_raw = models.CharField(max_length=128, null=True, blank=True, verbose_name=_("Logout Link"))
    show_change_password_link = models.BooleanField(default=False, verbose_name=_("Show Change Password Link"))
    change_password_link_raw = models.CharField(max_length=128, null=True, blank=True, verbose_name=_("Change Password Link"))


    def login_link(self):
        return get_url(self.login_link_raw)
    login_link.short_description = _("Login Link")

    def logout_link(self):
        return get_url(self.logout_link_raw)
    logout_link.short_description = _("Logout Link")

    def change_password_link(self):
        return get_url(self.change_password_link_raw)
    change_password_link.short_description = _("Change Password Link")

    msms_category = _("Django Power Cms Default Widgets")
    msms_priority = 1000

    class Meta:
        verbose_name = _("Topbar Widget")
        verbose_name_plural = _("Topbar Widgets")

    def render(self, request, global_context):
        context = {}
        context.update(global_context or {})
        brands = self.brands.all()
        context.update({
            "brands": brands,
            "welcome_message": self.get_welcome_message(request),
            "welcome_links": self.get_welcome_links(request),
        })
        return render_to_string("django-power-cms/widgets/topbar.html", context)

    def get_welcome_message(self, request):
        if request.user and request.user.pk:
            if not self.welcome_message_for_login_user:
                return ""
            else:
                return self.welcome_message_for_login_user.format(fullname=request.user.get_full_name())
        else:
            if not self.welcome_message_for_anonymous_user:
                return ""
            else:
                return self.welcome_message_for_anonymous_user
    
    def get_welcome_links(self, request):
        links = []
        change_password_link = self.get_change_password_link(request)
        if change_password_link:
            links.append(change_password_link)
        login_or_logout_link = self.get_login_or_logout_link(request)
        if login_or_logout_link:
            links.append(login_or_logout_link)
        links.reverse()
        return links

    def get_login_or_logout_link(self, request):
        if not self.show_login_or_logout_link:
            return None
        if request.user and request.user.pk:
            return {
                "class": "logout-link",
                "title": _("Logout"),
                "url": self.logout_link,
            }
        else:
            return {
                "class": "login-link",
                "title": _("Login"),
                "url": self.login_link,
            }

    def get_change_password_link(self, request):
        if not (self.show_change_password_link and request.user and request.user.pk):
            return None
        else:
            return {
                "class": "change-password-link",
                "title": _("Change password"),
                "url": self.change_password_link,
            }

class TopbarBrand(models.Model):
    topbar = models.ForeignKey(TopbarWidget, on_delete=models.CASCADE, related_name="brands", verbose_name=_("Topbar"))
    image = models.ImageField(upload_to="brand-images", null=True, blank=True, verbose_name=_("Image"))
    title = models.CharField(max_length=64, null=True, blank=True, verbose_name=_("Title"))
    url_raw = models.CharField(max_length=128, null=True, blank=True, verbose_name=_("URL"))
    order = models.IntegerField(default=0, verbose_name=_("Order"))

    class Meta:
        ordering = ["order"]
        verbose_name = _("Topbar Brand")
        verbose_name_plural = _("Topbar Brands")

    def __str__(self):
        return str(self.pk)

    def url(self):
        return get_url(self.url_raw)
    url.short_description = _("URL")

class Article(MPTTModel):
    TOP = _("Set Top")
    IMPORTANT = _("Important")
    GOOD_NEWS = _("Good News")
    WARNING = _("Warning")
    LABEL_CHOICES = [
        (TOP, TOP),
        (IMPORTANT, IMPORTANT),
        (GOOD_NEWS, GOOD_NEWS),
        (WARNING, WARNING),
    ]
    LABEL_CLASS_MAP = {
        str(TOP): "label label-primary",
        str(IMPORTANT): "label label-primary",
        str(GOOD_NEWS): "label label-success",
        str(WARNING): "label label-warning",
    }
    HIGH = 0
    NORAML = 99
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True, blank=True, default=admin_site_get_selected_site, related_name="articles", verbose_name=_("Site"))
    parent = TreeForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="children", limit_choices_to=limit_choices_to_selected_site, verbose_name=_("Article Parent"))
    title = models.CharField(max_length=64, verbose_name=_("Title"))
    author = models.CharField(max_length=64, null=True, blank=True, verbose_name=_("Author"))
    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))
    content = RichTextField(null=True, blank=True, verbose_name=_("Content"))
    published = models.BooleanField(verbose_name=_("Published"))
    published_time = models.DateTimeField(null=True, blank=True, verbose_name=_("Published Time"))
    preview_image = models.ImageField(upload_to="article-preview-images", null=True, blank=True, verbose_name=_("Preview Image"))
    show_preview_image = models.BooleanField(default=False, verbose_name=_("Show Preview Image"))
    order = models.IntegerField(null=True, blank=True, verbose_name=_("Order"))
    priority = models.IntegerField(default=99, verbose_name=_("Priority"))
    label = models.CharField(max_length=16, choices=LABEL_CHOICES, null=True, blank=True, verbose_name=_("Label"))

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")

    class MPTTMeta:
        order_insertion_by = ['order']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.label:
            self.priority = self.HIGH
        else:
            self.priority = self.NORAML
        if self.published and not self.published_time:
            self.published_time = timezone.now()
        elif not self.published and self.published_time:
            self.published_time = None
        return super().save(*args, **kwargs)

    @property
    def label_class(self):
        return self.LABEL_CLASS_MAP.get(self.label, "")

class ArticleContentImage(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="images", verbose_name=_("Article"))
    image = models.ImageField(upload_to="article-content-images", verbose_name=_("Image"))

    class Meta:
        verbose_name = _("Article Content Image")
        verbose_name_plural = _("Article Content Images")

    def __str__(self):
        return str(self.pk)

    def image_link(self):
        if not self.image:
            return ""
        else:
            return self.image.url
    image_link.short_description = _("Image Link")

class ArticleListWidget(Widget):
    root = models.ForeignKey("Article", on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Root"))
    article_list_page = models.ForeignKey(Page, on_delete=models.SET_NULL, related_name="+", null=True, blank=True, verbose_name=_("Article List Page"))
    article_page = models.ForeignKey(Page, on_delete=models.SET_NULL, related_name="+", null=True, blank=True, verbose_name=_("Article Page"))
    max_display_count = models.IntegerField(default=10, verbose_name=_("Max Display Count"))
    empty_display_message = models.TextField(null=True, blank=True, verbose_name=_("Empty Display Message"))

    msms_category = _("Django Power Cms Default Widgets")
    msms_priority = 5000

    class Meta:
        verbose_name = _("Article List Widget")
        verbose_name_plural = _("Article List Widgets")

    def render(self, request, global_context):
        if self.root:
            lists = self.root.children.filter(published=True).order_by("priority").all()[:self.max_display_count]
        else:
            lists = []
        return render_to_string("django-power-cms/widgets/article-list.html", {
            "lists": lists,
            "lists_length": len(lists),
            "empty_display_message": self.empty_display_message,
            "article_page": self.article_page,
            "article_list_page": self.article_list_page,
        })

class ArticleDetailWidget(Widget):
    root = models.ForeignKey("Article", on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Root"))
    show_description = models.BooleanField(default=False, verbose_name=_("Show Description"))
    show_published_time = models.BooleanField(default=True, verbose_name=_("Show Published Time"))
    show_author = models.BooleanField(default=False, verbose_name=_("Show Author"))
    show_prev_and_next_links = models.BooleanField(default=False, verbose_name=_("Show Prev&Next Links"))

    msms_category = _("Django Power Cms Default Widgets")
    msms_priority = 6000

    class Meta:
        verbose_name = _("Article Detail Widget")
        verbose_name_plural = _("Article Detail Widgets")

    def render(self, request, global_context):
        article_id= int(request.GET.get("article_id"))
        article = Article.objects.get(pk=article_id)
        if self.show_prev_and_next_links:
            prev = article.get_previous_sibling()
            next = article.get_next_sibling()
        else:
            prev = None
            next = None
        return render_to_string("django-power-cms/widgets/article-detail.html", {
            "article_id": article_id,
            "article": article,
            "show_description": self.show_description,
            "show_published_time": self.show_published_time,
            "show_prev_and_next_links": self.show_prev_and_next_links,
            "prev": prev,
            "next": next,
        })

class CardsWidget(Widget):
    card_width = models.CharField(default="25%", max_length=32, verbose_name=_("Card Width"))
    card_height = models.CharField(default="120px", max_length=32, verbose_name=_("Card Height"))
    image_width = models.CharField(default="80px", max_length=32, verbose_name=_("Image Width"))
    image_height = models.CharField(default="100px", max_length=32, verbose_name=_("Image Height"))
    title_height = models.CharField(default="30px", max_length=32, verbose_name=_("Title Height"))

    class Meta:
        verbose_name = _("Cards Widget")
        verbose_name_plural = _("Cards Widgets")

    css = [
        "django-power-cms/widgets/cards/css/cards.css",
    ]

    msms_category = _("Django Power Cms Default Widgets")
    msms_priority = 3500

    def render(self, request, global_context):
        context = {}
        context.update(global_context or {})
        context.update({
            "pk": self.pk,
            "card_width": self.card_width,
            "card_height": self.card_height,
            "image_width": self.image_width,
            "image_height": self.image_height,
            "title_height": self.title_height,
            "cards": self.items.all(),
        })
        return render_to_string("django-power-cms/widgets/cards.html", context)

class CardsItem(models.Model):
    widget = models.ForeignKey(CardsWidget, on_delete=models.CASCADE, related_name="items", verbose_name=_("Widget"))
    image = models.ImageField(upload_to="card-images", verbose_name=_("Image"))
    title = models.CharField(max_length=64, verbose_name=_("Title"))
    description = models.CharField(max_length=128, verbose_name=_("Description"), null=True, blank=True)
    order = models.IntegerField(default=0, verbose_name=_("Order"))
    url_raw = models.CharField(max_length=128, null=True, blank=True, verbose_name=_("URL"))
    open_url_in_new_window = models.BooleanField(default=False, verbose_name=_("Open URL In New Window"))

    class Meta:
        verbose_name = _("Card Item")
        verbose_name_plural = _("Card Items")
        ordering = ["order"]

    def __str__(self):
        return str(self.pk)

    def url(self):
        return get_url(self.url_raw)
    url.short_description = _("URL")
