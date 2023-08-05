# django-power-cms

A power content management system based on django admin framework.

## Install

```shell
pip install django-power-cms
```

## Release

### v0.3.3 2020/04/03

1. Fix django-changelist-toolbar-admin upgraded problem.
1. Fix fontawesome css missing problem in portlet registering.

### v0.3.2 2020/03/31

1. Add Widget type categorizing and sorting support.
1. Add site limit to page widget in page changeform.
1. Add CardsWidth support.
1. PageWidget's slot options dynamically changes with page's template value.
1. Change topbar brand style.

### v0.3.1 2020/03/22

1. Site use a tabbed changeform.
1. Widget use a tabbed changeform.
1. Article use a tabbed changeform.
1. Set Page's site field to current selected site.
1. Set Widget's site field to current selected site.
1. Set Article's site field to current selected site.
1. Limit Page queryset to current selected site.
1. Limit Widget queryset to current selected site.
1. Limit Article queryset to current selected site.
1. Add template preview images.
1. Command django-power-cms-template add register-all sub-command.
1. Command django-power-cms-theme add register-all sub-command.
1. Add page's parent filed limit choice to current selected site.
1. Add article's parent field limit choice to current selected site.
1. Add preview link in site changelist card.
1. Fix requirements.txt missing libraries problem.

### v0.3.0 2020/03/21

1. Add no-portlet template.
1. Add site's facicon.
1. Add page title.
1. Add article detail widget.
1. Article model add site field.
1. Save current site id in session, and pages/wigets/articles are filtered with the site id.
1. Fix topbar's brand-image and brand-title display position problem.
1. Default template use full screen size instead of 1170px width.
1. Topbar brand link supports site-code-url and page-code-url.

### v0.2.0 2020/03/08

1. Add left-portlet, both-portlet template support.
1. Add template and theme register commands.
1. Add page preview button.
1. Allow same page code in different site.
1. Turn site admin style to django-cards-admin.

### v0.1.0 2020/03/05

1. First release.
