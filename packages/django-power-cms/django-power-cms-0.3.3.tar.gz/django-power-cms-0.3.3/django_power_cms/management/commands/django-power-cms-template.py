import djclick as click
import yaml
import pprint
from magic_import import import_from_string
from django_power_cms.models import Template


@click.group()
def register():
    """Django-Power-Site-Template register service.
    """

@register.command()
def scan():
    """Scan and list all avaiable templates.
    """
    from django.apps import apps
    counter = 0
    for app_config in apps.get_app_configs():
        name = app_config.name + ".export_templates.templates"
        templates = import_from_string(name) or []
        for template in templates:
            counter += 1
            app_label = template.get("app_label", "")
            code = template.get("code", "")
            name = template.get("name", "")
            print("{0}\t{1}\t{2}\t{3}".format(counter, app_label, code, name))

@register.command(name="register")
@click.argument("code", nargs=1, required=True)
def register_by_code(code):
    """Register or update template by template code.
    """
    found = False
    from django.apps import apps
    for app_config in apps.get_app_configs():
        name = app_config.name + ".export_templates.templates"
        templates = import_from_string(name) or []
        for template in templates:
            template_code = template.get("code", "")
            template_name = template.get("name", "")
            app_label = template.get("app_label", "")
            if code == template_code:
                found = True
                Template.register(template)
                print("Template registered: {0} {1} {2}".format(app_label, template_code, template_name))
                break
    if not found:
        print("Template with code: {0} NOT found.".format(code))

@register.command(name="register-all")
def register_all():
    """Register or update all templates.
    """
    found = False
    from django.apps import apps
    for app_config in apps.get_app_configs():
        name = app_config.name + ".export_templates.templates"
        templates = import_from_string(name) or []
        for template in templates:
            template_code = template.get("code", "")
            template_name = template.get("name", "")
            app_label = template.get("app_label", "")
            found = True
            Template.register(template)
            print("Template registered: {0} {1} {2}".format(app_label, template_code, template_name))
    if not found:
        print("Template with code: {0} NOT found.".format(code))