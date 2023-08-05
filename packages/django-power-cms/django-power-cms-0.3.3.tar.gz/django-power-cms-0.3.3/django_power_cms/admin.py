import re
from django.contrib import admin
from django.forms import ModelForm
from django.urls import reverse
from django.templatetags.static import static
from django.utils.html import mark_safe
from django.contrib.admin.options import csrf_protect_m
from mptt.admin import DraggableMPTTAdmin
from mptt.admin import TreeRelatedFieldListFilter
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from django_readedit_switch_admin.admin import DjangoReadEditSwitchAdmin
from django_changelist_toolbar_admin.admin import DjangoChangelistToolbarAdmin
from django_visit_on_site_in_new_window.admin import DjangoVisitOnSiteInNewWindowAdmin
from django_cards_admin.admin import DjangoCardsAdminMixin
from django_msms_admin.admin import DjangoMsmsAdmin
from django_msms_admin.admin import DjangoSubclassAdmin
from django_tabbed_changeform_admin.admin import DjangoTabbedChangeformAdmin
from django_force_disable_permissions_admin.admin import DjagnoForceDisablePermissionsAdminMixin
from django_toggle_switch_widget.widgets import DjangoToggleSwitchWidget
from django_gazing_select_widget.widgets import DjangoGazingSelectWidget
from django_mptt_simple_listfilters.filters import ListFilterIgnoreLeafNodes
from .settings import CURRENT_SIET_ID_SESSION_KEY
from .models import Template
from .models import TemplateSlot
from .models import Site
from .models import Page
from .models import PageWidget
from .models import Widget
from .models import StaticHtmlWidget
from .models import CarouselWidget
from .models import CarouselWidgetImage
from .models import Theme
from .models import ThemeCss
from .models import ThemeJs
from .models import WidgetLink
from .models import StaticListWidget
from .models import StaticListItem
from .models import TopbarWidget
from .models import TopbarBrand
from .models import Article
from .models import ArticleContentImage
from .models import ArticleListWidget
from .models import ArticleDetailWidget
from .models import CardsWidget
from .models import CardsItem


class TemplateSlotInline(DjangoReadEditSwitchAdmin, admin.TabularInline):
    model = TemplateSlot
    extra = 0

class TemplateAdmin(DjagnoForceDisablePermissionsAdminMixin, admin.ModelAdmin):
    force_disable_add_permission = True
    force_disable_change_permission = True
    force_disable_delete_permission = True

    class Media:
        css = {
            "all": [
                "django-power-cms/admin/fix-template-style.css",
            ]
        }

    list_display = ["name", "preview", "app_verbose_name", "description"]
    list_display_links = list_display
    list_filter = ["app_verbose_name"]
    search_fields = ["name", "app_label", "app_verbose_name", "description", "template"]
    inlines = [
        TemplateSlotInline,
    ]
    fieldsets = [
        (None, {
            "fields": [("code", "name"), ("app_label", "app_verbose_name"), ("description", "template"), "preview"]
        })
    ]
    readonly_fields = ["preview"]

    def preview(self, obj):
        url = static(obj.preview_image)
        return mark_safe("""<img src="{url}" class="template-preview-image" />""".format(url=url))
    preview.short_description = _("Preview")

class ThemeCssInline(DjagnoForceDisablePermissionsAdminMixin, admin.TabularInline):
    force_disable_add_permission = True
    force_disable_change_permission = True
    force_disable_delete_permission = True
    model = ThemeCss
    extra = 0

class ThemeJsInline(DjagnoForceDisablePermissionsAdminMixin, admin.TabularInline):
    force_disable_add_permission = True
    force_disable_change_permission = True
    force_disable_delete_permission = True
    model = ThemeJs
    extra = 0

class ThemeForm(ModelForm):
    class Meta:
        model = Theme
        exclude = []
        widgets = {
            "is_default": DjangoToggleSwitchWidget(klass="django-toggle-switch-primary"),
        }

class ThemeAdmin(DjangoReadEditSwitchAdmin, DjagnoForceDisablePermissionsAdminMixin, admin.ModelAdmin):

    class Media:
        css = {
            "all": [
                "django-power-cms/admin/fix-theme-style.css",
            ]
        }
    force_disable_add_permission = True
    force_disable_delete_permission = True

    form = ThemeForm
    list_display = ["name", "description", "is_default"]
    list_filter = ["is_default"]
    search_fields = ["name", "description"]
    inlines = [
        ThemeCssInline,
        ThemeJsInline,
    ]

    fieldsets = [
        (None, {
            "fields": [("code", "name"), ("app_label", "app_verbose_name"), ("description", "is_default"), "preview"]
        })
    ]
    readonly_fields = ["code", "name", "app_label", "app_verbose_name", "description", "preview"]

    def preview(self, obj):
        url = static(obj.preview_image)
        return mark_safe("""<img src="{url}" class="theme-preview-image" />""".format(url=url))
    preview.short_description = _("Preview")

class SiteForm(ModelForm):
    class Meta:
        model = Site
        exclude = []
        widgets = {
            "published": DjangoToggleSwitchWidget(klass="django-toggle-switch-primary"),
        }

class SiteAdmin(
        DjangoReadEditSwitchAdmin,
        DjangoCardsAdminMixin,
        DjangoVisitOnSiteInNewWindowAdmin,
        DjangoTabbedChangeformAdmin,
        admin.ModelAdmin):
    form = SiteForm
    result_cards_columns = 3
    list_display = ["name", "code", "published", "published_time", "preview_link"]
    search_fields = ["name", "code"]
    readonly_fields = ["published_time"]
    result_card_body_height = 200
    fieldsets = [
        (None, {
            "fields": ["name", "code", "theme", "index_page_code"],
            "classes": ["tab-basic"],
        }),
        (_("Publish State"), {
            "fields": ["published", "published_time"],
            "classes": ["tab-publish"],
        }),
        (_("Other Config"), {
            "fields": ["favicon"],
            "classes": ["tab-other"],
        }),
    ]
    tabs = [
        (_("Basic Info"), ["tab-basic", "tab-publish"]),
        (_("Other Config"), ["tab-other"]),
    ]

    def preview_link(self, obj):
        return format_html(
            """<a href="{0}" target="_blank">{1}</a>""",
            obj.get_absolute_url(),
            _("Preview"),
        )

    preview_link.short_description = _("Preview")

    class Media:
        css = {
            "all": [
                "fontawesome/css/all.min.css",
            ]
        }

    def result_card_link_title(self, item):
        return _("Enter into Site Manager...")

    @csrf_protect_m
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        if object_id:
            request.session[CURRENT_SIET_ID_SESSION_KEY] = object_id
        return super().changeform_view(request, object_id, form_url, extra_context)

def get_all_template_slots():
    slots = [
        ("", "-"*10),
    ]
    for slot in TemplateSlot.objects.order_by("template", "order").all():
        slots.append((slot.pk, slot.template.name + "." + slot.name))
    return slots

def get_choices_related():
    choices_related = {}
    for slot in TemplateSlot.objects.order_by("template", "order").all():
        choices_related[slot.pk] = [str(slot.template.pk)]
    return choices_related

class PageWidgetForm(ModelForm):
    class Meta:
        model = PageWidget
        exclude = []
        widgets = {
            "slot": DjangoGazingSelectWidget(
                gazing_field_name="template",
                this_field_name="slot",
                choices_related=get_choices_related,
                gazing_related=False,
                choices=get_all_template_slots,
                )
        }

class PageWidgetInline(DjangoReadEditSwitchAdmin, admin.TabularInline):
    form = PageWidgetForm
    model = PageWidget
    extra = 0
    classes = ["tab-page-widgets"]

class PageAdmin(
        DjangoReadEditSwitchAdmin,
        DjangoChangelistToolbarAdmin,
        DjangoVisitOnSiteInNewWindowAdmin,
        DjangoTabbedChangeformAdmin,
        DraggableMPTTAdmin,
        admin.ModelAdmin):
    list_display = ["tree_actions", "display_title", "display_page_url", "template", "preview_link"]
    list_display_links = ["display_title"]

    def display_title(self, obj):
        return format_html(
            '<div style="text-indent:{}px">{}</div>',
            obj._mpttfield('level') * self.mptt_level_indent,
            obj.name,
        )
    display_title.short_description = _('Title')

    def display_page_url(self, obj):
        return "page:{0}:{1}".format(obj.site.code, obj.code)
    display_page_url.short_description = _("Display Page URL") 

    def preview_link(self, obj):
        return format_html(
            """<a href="{0}" target="_blank">{1}</a>""",
            obj.get_absolute_url(),
            _("Preview"),
        )
    preview_link.short_description = _("Preview")

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        site_id = request.session.get(CURRENT_SIET_ID_SESSION_KEY, None)
        if site_id:
            return queryset.filter(site__id=int(site_id))
        else:
            return queryset.none()

    readonly_fields = ["site", "published_time"]
    fieldsets = [
        (None, {
            "fields": ["site", "parent", "name", "code"],
            "classes": ["tab-basic"],
        }),
        (None, {
            "fields": ["template", "theme"],
            "classes": ["tab-site-styles"],
        }),
        (_("Publish Status"), {
            "fields": ["published", "published_time"],
            "classes": ["tab-publish"],
        })
    ]
    inlines = [
        PageWidgetInline,
    ]
    tabs = [
        (_("Page Basic Settings"), ["tab-basic", "tab-site-style", "tab-publish"]),
        (_("Page Template & Theme Settings"), ["tab-site-styles"]),
        (_("Page Widgets Settings"), ["tab-page-widgets"]),
    ]

class ArticleContentImageInline(admin.TabularInline):
    model = ArticleContentImage
    extra = 0
    fieldsets = [
        (None, {
            "fields": ["image", "image_link"],
        }),
    ]
    readonly_fields = ["image_link"]
    classes = ["tab-content-images"]

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        exclude = []
        widgets = {
            "published": DjangoToggleSwitchWidget(klass="django-toggle-switch-primary"),
        }

class ArticleAdmin(
        DjangoReadEditSwitchAdmin,
        DraggableMPTTAdmin,
        DjangoTabbedChangeformAdmin,
        DjangoChangelistToolbarAdmin,
        admin.ModelAdmin):
    form = ArticleForm
    list_display = ["tree_actions", "indented_title", "published", "published_time", "label"]
    list_display_links = ["indented_title"]
    list_filter = [
        ("parent", ListFilterIgnoreLeafNodes),
    ]
    readonly_fields = ["site", "published_time"]

    def display_title(self, instance):
        return format_html(
            '<div style="text-indent:{}px">{}</div>',
            instance._mpttfield('level') * self.mptt_level_indent,
            instance.title,
        )
    display_title.short_description = _('Title')

    fieldsets = [
        (None, {
            "fields": ["site", "parent", "title", "description", "label"],
            "classes": ["tab-basic"],
        }),
        (_("Article Publish Settings"), {
            "fields": ["published", "published_time"],
            "classes": ["tab-publish"]
        }),
        (None, {
            "fields": ["content", "preview_image", "show_preview_image"],
            "classes": ["tab-content"],
        }),

    ]
    inlines = [
        ArticleContentImageInline
    ]

    tabs = [
        (_("Article Basic Settings"), ["tab-basic", "tab-publish"]),
        (_("Article Content Settings"), ["tab-content"]),
        (_("Article Content Image Settigns"), ["tab-content-images"]),
    ]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        site_id = request.session.get(CURRENT_SIET_ID_SESSION_KEY, None)
        if site_id:
            return queryset.filter(site__id=int(site_id))
        else:
            return queryset.none()

class WidgetLinkInline(admin.TabularInline):
    model = WidgetLink
    extra = 0
    classes = ["tab-widget-links"]

class WidgetAdminBase(
        DjangoTabbedChangeformAdmin,
        DjangoReadEditSwitchAdmin,
        admin.ModelAdmin):
    list_display = ["name", "type_name"]
    list_filter = ["type_name"]
    search_fields = ["name"]
    fieldsets = [
        (None, {
            "fields": ["site", "name"],
            "classes": ["tab-widget-basic"]
        }),
        (_("Widget Basic Style Settings"), {
            "fields": ["title", "widget_with_border", "widget_body_padding"],
            "classes": ["tab-widget-basic-style"],
        }),
        (None, {
            "fields": ["widget_class", "widget_header_class", "widget_body_class", "widget_footer_class"],
            "classes": ["tab-widget-extra-classes"],
        }),
        (None, {
            "fields": ["widget_style", "widget_header_style", "widget_body_style", "widget_footer_style"],
            "classes": ["tab-widget-inline-style"],
        })
    ]
    readonly_fields = ["site"]
    
    tabs = [
        (_("Widget Basic Settings"), ["tab-widget-basic", "tab-widget-basic-style"]),
        (_("Widget Extra Class"), ["tab-widget-extra-classes"]),
        (_("Widget Inline Style"), ["tab-widget-inline-style"]),
        (_("Widget Links"), ["tab-widget-links"]),
    ]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        site_id = request.session.get(CURRENT_SIET_ID_SESSION_KEY, None)
        if site_id:
            return queryset.filter(site__id=int(site_id))
        else:
            return queryset.none()

class WidgetAdmin(
        DjangoMsmsAdmin,
        WidgetAdminBase,
        admin.ModelAdmin):
    pass

class StaticHtmlWidgetAdmin(DjangoSubclassAdmin, WidgetAdminBase, admin.ModelAdmin):
    inlines = [
        WidgetLinkInline,
    ]
    fieldsets = WidgetAdminBase.fieldsets + [
        (None, {
            "fields": ["html"],
            "classes": ["tab-static-html"],
        })
    ]
    def get_tabs(self, request, object_id, form_url, extra_context):
        tabs = super().get_tabs(request, object_id, form_url, extra_context)
        tabs.insert(1, (_("Static Html Settings"), ["tab-static-html"]))
        return tabs

class CarouselWidgetImageInline(admin.TabularInline):
    model = CarouselWidgetImage
    extra = 0
    classes = ["tab-carouse-images"]

class CarouselWidgetAdmin(DjangoSubclassAdmin, WidgetAdminBase, admin.ModelAdmin):
    inlines = [
        WidgetLinkInline,
        CarouselWidgetImageInline,
    ]
    def get_tabs(self, request, object_id, form_url, extra_context):
        tabs = super().get_tabs(request, object_id, form_url, extra_context)
        tabs.insert(1, (_("Carouse Widget Image Settings"), ["tab-carouse-images"]))
        return tabs

class StaticListItemInline(admin.StackedInline):
    model = StaticListItem
    extra = 0
    fieldsets = [
        [None, {
            "fields": [
                ("title", "url"),
                ("target", "order"),
                ("label", "label_class"),
            ]
        }]
    ]
    classes = ["tab-static-list-items"]

class StaticListWidgetAdmin(DjangoSubclassAdmin, WidgetAdminBase, admin.ModelAdmin):
    inlines = [
        WidgetLinkInline,
        StaticListItemInline,
    ]
    def get_tabs(self, request, object_id, form_url, extra_context):
        tabs = super().get_tabs(request, object_id, form_url, extra_context)
        tabs.insert(1, (_("Static List Item Settings"), ["tab-static-list-items"]))
        return tabs

class TopbarBrandInline(admin.TabularInline):
    model = TopbarBrand
    extra = 0
    classes = ["tab-topbar-brands"]

class TopbarWidgetAdmin(DjangoSubclassAdmin, WidgetAdminBase, admin.ModelAdmin):
    inlines = [
        WidgetLinkInline,
        TopbarBrandInline,
    ]
    fieldsets = WidgetAdminBase.fieldsets + [
        (None, {
            "fields": ["fix_position"],
            "classes": ["tab-topbar-basic"],
        }),
        (_("Welcome message settings"), {
            "fields": ["welcome_message_for_login_user", "welcome_message_for_anonymous_user"],
            "classes": ["tab-welcome-message"],
        }),
        (_("Change password link settings"), {
            "fields": ["show_change_password_link", "change_password_link_raw"],
            "classes": ["tab-change-password"],
        }),
        (_("Login and logout link Settings"), {
            "fields": ["show_login_or_logout_link", "login_link_raw", "logout_link_raw"],
            "classes": ["tab-login-or-logout-link"]
        })
    ]
    def get_tabs(self, request, object_id, form_url, extra_context):
        tabs = super().get_tabs(request, object_id, form_url, extra_context)
        tabs.insert(1, (_("Topbar Brand Settings"), ["tab-topbar-brands"]))
        tabs.insert(2, (_("Topbar Settings"), ["tab-topbar-basic", "tab-welcome-message", "tab-change-password", "tab-login-or-logout-link"]))
        return tabs

class ArticleListWidgetAdmin(DjangoSubclassAdmin, WidgetAdminBase, admin.ModelAdmin):
    inlines = [
        WidgetLinkInline,
    ]
    fieldsets = WidgetAdminBase.fieldsets + [
        (None, {
            "fields": ["root", "article_list_page", "article_page", "max_display_count", "empty_display_message"],
            "classes": ["tab-article-list-settings"]
        })
    ]
    def get_tabs(self, request, object_id, form_url, extra_context):
        tabs = super().get_tabs(request, object_id, form_url, extra_context)
        tabs.insert(1, (_("Article List Settings"), ["tab-article-list-settings"]))
        return tabs

class ArticleDetailWidgetAdmin(DjangoSubclassAdmin, WidgetAdminBase, admin.ModelAdmin):
    inlines = [
        WidgetLinkInline,
    ]
    fieldsets = WidgetAdminBase.fieldsets + [
        (None, {
            "fields": ["root", "show_description", "show_published_time", "show_author", "show_prev_and_next_links"],
            "classes": ["tab-article-detail-settings"]
        })
    ]
    def get_tabs(self, request, object_id, form_url, extra_context):
        tabs = super().get_tabs(request, object_id, form_url, extra_context)
        tabs.insert(1, (_("Article Detail Settings"), ["tab-article-detail-settings"]))
        return tabs

class CardsItemInline(admin.TabularInline):
    model = CardsItem
    extra = 0
    classes = ["tab-cards-items"]

class CardsWidgetAdmin(DjangoSubclassAdmin, WidgetAdminBase, admin.ModelAdmin):
    inlines = [
        WidgetLinkInline,
        CardsItemInline
    ]
    fieldsets = WidgetAdmin.fieldsets + [
        (None, {
            "fields": ["card_width", "card_height", "image_width", "image_height", "title_height"],
            "classes": ["tab-cards-widget-basic-settings"]
        })
    ]
    def get_tabs(self, request, object_id, form_url, extra_context):
        tabs = super().get_tabs(request, object_id, form_url, extra_context)
        tabs.insert(1, (_("Cards Widget Settings"), ["tab-cards-widget-basic-settings", "tab-cards-items"]))
        return tabs

admin.site.register(Site, SiteAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Article, ArticleAdmin)

admin.site.register(Widget, WidgetAdmin)
admin.site.register(CarouselWidget, CarouselWidgetAdmin)
admin.site.register(StaticHtmlWidget, StaticHtmlWidgetAdmin)
admin.site.register(StaticListWidget, StaticListWidgetAdmin)
admin.site.register(TopbarWidget, TopbarWidgetAdmin)
admin.site.register(ArticleListWidget, ArticleListWidgetAdmin)
admin.site.register(ArticleDetailWidget, ArticleDetailWidgetAdmin)
admin.site.register(CardsWidget, CardsWidgetAdmin)

admin.site.register(Template, TemplateAdmin)
admin.site.register(Theme, ThemeAdmin)
