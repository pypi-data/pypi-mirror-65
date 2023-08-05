from django.urls import path
from . import views


urlpatterns = [
    path('<site_code>/', views.site, name="django-power-cms.site"),
    path('<site_code>/<page_code>/', views.page, name="django-power-cms.page"),
    
 ]
 