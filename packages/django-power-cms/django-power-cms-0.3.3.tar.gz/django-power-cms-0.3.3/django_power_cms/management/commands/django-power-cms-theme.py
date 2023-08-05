import djclick as click
import yaml
import pprint
from magic_import import import_from_string
from django_power_cms.models import Theme


@click.group()
def register():
    """Django-Power-Site-Theme register service.
    """

@register.command()
def scan():
    """Scan and list all avaiable themes.
    """
    from django.apps import apps
    counter = 0
    for app_config in apps.get_app_configs():
        name = app_config.name + ".export_themes.themes"
        themes = import_from_string(name) or []
        for theme in themes:
            counter += 1
            app_label = theme.get("app_label", "")
            code = theme.get("code", "")
            name = theme.get("name", "")
            print("{0}\t{1}\t{2}\t{3}".format(counter, app_label, code, name))

@register.command(name="register")
@click.argument("code", nargs=1, required=True)
def register_by_code(code):
    """Register or update theme by theme code.
    """
    found = False
    from django.apps import apps
    for app_config in apps.get_app_configs():
        name = app_config.name + ".export_themes.themes"
        themes = import_from_string(name) or []
        for theme in themes:
            theme_code = theme.get("code", "")
            theme_name = theme.get("name", "")
            app_label = theme.get("app_label", "")
            if code == theme_code:
                found = True
                Theme.register(theme)
                print("Theme registered: {0} {1} {2}".format(app_label, theme_code, theme_name))
                break
    if not found:
        print("Theme with code: {0} NOT found.".format(code))

@register.command(name="register-all")
def register_all():
    """Register or update all themes.
    """
    found = False
    from django.apps import apps
    for app_config in apps.get_app_configs():
        name = app_config.name + ".export_themes.themes"
        themes = import_from_string(name) or []
        for theme in themes:
            theme_code = theme.get("code", "")
            theme_name = theme.get("name", "")
            app_label = theme.get("app_label", "")
            found = True
            Theme.register(theme)
            print("Theme registered: {0} {1} {2}".format(app_label, theme_code, theme_name))
    if not found:
        print("Theme with code: {0} NOT found.".format(code))
