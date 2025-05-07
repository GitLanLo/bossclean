from django.urls import path, re_path, register_converter
from . import views
from . import converters

register_converter(converters.FourDigitYearConverter, "year4")
urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('tag/<slug:tag_slug>/', views.show_tag_services, name='tag'),
    path('services/<slug:service_slug>/', views.show_service, name='service_detail'),
    path('category/<slug:cat_slug>/', views.show_category, name='category'),
    path('addpage/', views.addpage, name='add_page'),
     path('contact/', views.contact, name='contact'),
     path('login/', views.login, name='login'),
    path('categories/<int:so_id>/', views.categories, name='so_int'),
    path('categories/<slug:so_slug>/', views.categoriesBySlug, name='so_slug'),
    path('archive/<year4:year>/', views.archive, name='archive'),

]