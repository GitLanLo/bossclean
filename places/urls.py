from django.urls import path, re_path, register_converter
from . import views
from . import converters
from django.urls import path
from .views import gpt_chat, gpt_chat_ajax

register_converter(converters.FourDigitYearConverter, "year4")
urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('tag/<slug:tag_slug>/', views.show_tag_services, name='tag'),
    path('services/<slug:service_slug>/', views.show_service, name='service_detail'),
    path('category/<slug:cat_slug>/', views.show_category, name='category'),
    path('add_request/', views.add_request, name='add_request'),
    path('order_success/<int:order_id>/', views.order_success, name='order_success'),
    path('my_orders/', views.MyOrdersView.as_view(), name='my_orders'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
     path('contact/', views.contact, name='contact'),
     path('login/', views.login, name='login'),
    path('categories/<int:so_id>/', views.categories, name='so_int'),
    path('categories/<slug:so_slug>/', views.categoriesBySlug, name='so_slug'),
    path('archive/<year4:year>/', views.archive, name='archive'),
    path("gpt-chat/", gpt_chat, name="gpt_chat"),
    path("gpt-chat-ajax/", gpt_chat_ajax, name="gpt_chat_ajax"),
]

