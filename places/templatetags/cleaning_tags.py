from django import template
import places.views as views

register = template.Library()

@register.simple_tag(name='get_services')
def get_services():
    return views.services_db

@register.inclusion_tag('places/list_services_chast.html')
def show_services(srv_select=0):
    return {'services': views.services_db, 'srv_select': srv_select}

