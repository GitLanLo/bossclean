from django.urls import path, re_path, register_converter
from . import views
from . import converters

register_converter(converters.FourDigitYearConverter, "year4")
urlpatterns = [
    path('', views.index, name='index'),
    path('categories/<int:so_id>/', views.categories, name='so_int'),
    path('categories/<slug:so_slug>/', views.categoriesBySlug, name='so_slug'),
    path('archive/<year4:year>/', views.archive, name='archive'),

]