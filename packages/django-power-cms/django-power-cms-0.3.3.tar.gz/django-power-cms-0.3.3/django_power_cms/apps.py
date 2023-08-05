from django.apps import AppConfig
from django_admin_app_sidebar.portlets import register_portlet
from django_admin_app_sidebar.portlets import SidebarNavigation
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.urls import reverse

class DjangoPowerCmsConfig(AppConfig):
    name = 'django_power_cms'
    verbose_name = _("Django Power CMS")

    def ready(self):
        self.register_app_navigation_portlet()
        self.model_list_reorder()

    def get_site_config_url(self, request, *args, **kwargs):
        from .settings import CURRENT_SIET_ID_SESSION_KEY
        try:
            site_id = request.session[CURRENT_SIET_ID_SESSION_KEY]
            return reverse("admin:{}_{}_change".format(self.name, "site"), kwargs={"object_id": int(site_id)})
        except:
            return """javascript:alert("请先选择站点！");"""

    def get_page_manager_url(self, request, *args, **kwargs):
        from .settings import CURRENT_SIET_ID_SESSION_KEY
        try:
            site_id = request.session[CURRENT_SIET_ID_SESSION_KEY]
            return reverse("admin:{}_{}_changelist".format(self.name, "page"))
        except:
            return """javascript:alert("请先选择站点！");"""

    def get_widget_manager_url(self, request, *args, **kwargs):
        from .settings import CURRENT_SIET_ID_SESSION_KEY
        try:
            site_id = request.session[CURRENT_SIET_ID_SESSION_KEY]
            return reverse("admin:{}_{}_changelist".format(self.name, "widget"))
        except:
            return """javascript:alert("请先选择站点！");"""

    def get_article_manager_url(self, request, *args, **kwargs):
        from .settings import CURRENT_SIET_ID_SESSION_KEY
        try:
            site_id = request.session[CURRENT_SIET_ID_SESSION_KEY]
            return reverse("admin:{}_{}_changelist".format(self.name, "article"))
        except:
            return """javascript:alert("请先选择站点！");"""

    def register_app_navigation_portlet(self):
        nav = SidebarNavigation(_("Site Manager"), [{
            "title": "站点选择",
            "url": reverse_lazy("admin:{0}_{1}_changelist".format(self.name, "site")),
            "icon": "fas fa-globe",
            "depth": 1,
        }, {
            "title": "站点设置",
            "url": self.get_site_config_url,
            "icon": "fas fa-cog",
            "depth": 1,
        }, "-", {
            "title": _("Page Manager"),
            "url": self.get_page_manager_url,
            "icon": "fas fa-object-group",
            "depth": 1,
        }, {
            "title": _("Widget Manager"),
            "url": self.get_widget_manager_url,
            "icon": "fas fa-th",
            "depth": 1,
        }, {
            "title": _("Article Manager"),
            "url": self.get_article_manager_url,
            "icon": "fas fa-newspaper",
            "depth": 1,
        }])
        register_portlet(nav, app_label=self.name, model_name="site", extra_css=["fontawesome/css/all.min.css"])
        register_portlet(nav, app_label=self.name, model_name="page", extra_css=["fontawesome/css/all.min.css"])
        register_portlet(nav, app_label=self.name, model_name="widget", extra_css=["fontawesome/css/all.min.css"])
        register_portlet(nav, app_label=self.name, model_name="article", extra_css=["fontawesome/css/all.min.css"])

    def model_list_reorder(self):
        from django.conf import settings
        if hasattr(settings, "ADMIN_REORDER"):
            for app_index in range(len(settings.ADMIN_REORDER)):
                app_setting = settings.ADMIN_REORDER[app_index]
                if isinstance(app_setting, str):
                    if app_setting != "django_power_cms":
                        continue
                    else:
                        app_setting = {"app": "django_power_cms"}
                        settings.ADMIN_REORDER[app_index] = app_setting
                else:
                    if app_setting["app"] != "django_power_cms":
                        continue
                app_setting["models"] =  [
                    {"model":  'django_power_cms.Site', "label": _("Site Manager")},
                    {"model": 'django_power_cms.Template', "label": _("Template Manager")},
                    {"model": 'django_power_cms.Theme', "label": _("Theme Manager")},
                ]
