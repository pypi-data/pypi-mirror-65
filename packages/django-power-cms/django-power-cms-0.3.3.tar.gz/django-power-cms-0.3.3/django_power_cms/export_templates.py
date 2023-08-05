from django_power_cms.apps import DjangoPowerCmsConfig
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

language_code = settings.LANGUAGE_CODE.lower().replace("-", "_")

templates = [{
    "code": "4ef1dbc1256149a09d6ea9b23b09a7a8",
    "name": _("Right Portlet Template"),
    "app_label": "django_power_cms",
    "app_verbose_name": DjangoPowerCmsConfig.verbose_name,
    "description": _("Right Portlet Template Description."),
    "preview_image": "django-power-cms/templates/right-portlet/img/right-portlet-{language_code}.png".format(language_code=language_code),
    "template": "django-power-cms/templates/right-portlet.html",
    "slots": [{
        "code": "topbars",
        "name": _("Slot Topbars"),
        "order": 1,
    },{
        "code": "headers",
        "name": _("Slot Headers"),
        "order": 2,
    },{
        "code": "mains",
        "name": _("Slot Mains"),
        "order": 3,
    },{
        "code": "right_portlets",
        "name": _("Right Slot Portlets"),
        "order": 4,
    },{
        "code": "footers",
        "name": _("Slot Footers"),
        "order": 5,
    }]
},{
    "code": "811ec1329c7f4d9b9d874090d6094cec",
    "name": _("Left Portlet Template"),
    "app_label": "django_power_cms",
    "app_verbose_name": DjangoPowerCmsConfig.verbose_name,
    "description": _("Left Portlet Template Description."),
    "preview_image": "django-power-cms/templates/left-portlet/img/left-portlet-{language_code}.png".format(language_code=language_code),
    "template": "django-power-cms/templates/left-portlet.html",
    "slots": [{
        "code": "topbars",
        "name": _("Slot Topbars"),
        "order": 1,
    },{
        "code": "headers",
        "name": _("Slot Headers"),
        "order": 2,
    },{
        "code": "mains",
        "name": _("Slot Mains"),
        "order": 3,
    },{
        "code": "left_portlets",
        "name": _("Left Slot Portlets"),
        "order": 4,
    },{
        "code": "footers",
        "name": _("Slot Footers"),
        "order": 5,
    }]
},{
    "code": "84121a8a2a77470bb958df38711a5ea2",
    "name": _("Both Portlet Template"),
    "app_label": "django_power_cms",
    "app_verbose_name": DjangoPowerCmsConfig.verbose_name,
    "description": _("Both Portlet Template Description."),
    "preview_image": "django-power-cms/templates/both-portlet/img/both-portlet-{language_code}.png".format(language_code=language_code),
    "template": "django-power-cms/templates/both-portlet.html",
    "slots": [{
        "code": "topbars",
        "name": _("Slot Topbars"),
        "order": 1,
    },{
        "code": "headers",
        "name": _("Slot Headers"),
        "order": 2,
    },{
        "code": "left_portlets",
        "name": _("Left Slot Portlets"),
        "order": 3,
    },{
        "code": "mains",
        "name": _("Slot Mains"),
        "order": 4,
    },{
        "code": "right_portlets",
        "name": _("Right Slot Portlets"),
        "order": 5,
    },{
        "code": "footers",
        "name": _("Slot Footers"),
        "order": 6,
    }]
},{
    "code": "5aa2b1690ee84e8697d9aecbb25d17d3",
    "name": _("No Portlet Template"),
    "app_label": "django_power_cms",
    "app_verbose_name": DjangoPowerCmsConfig.verbose_name,
    "description": _("No Portlet Template Description."),
    "preview_image": "django-power-cms/templates/no-portlet/img/no-portlet-{language_code}.png".format(language_code=language_code),
    "template": "django-power-cms/templates/no-portlet.html",
    "slots": [{
        "code": "topbars",
        "name": _("Slot Topbars"),
        "order": 1,
    },{
        "code": "headers",
        "name": _("Slot Headers"),
        "order": 2,
    },{
        "code": "mains",
        "name": _("Slot Mains"),
        "order": 3,
    },{
        "code": "footers",
        "name": _("Slot Footers"),
        "order": 4,
    }]
}]
