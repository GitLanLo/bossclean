from django import template
import places.views as views
from places.models import ServiceCategory, TagService

register = template.Library()

@register.simple_tag(name='get_services')
def get_services():
    return views.services_db

@register.inclusion_tag('places/list_services_chast.html')
def show_services(srv_select=0):
    return {'services': views.services_db, 'srv_select': srv_select}

@register.inclusion_tag('places/list_categories.html')
def show_categories(cat_selected=0):
    cats = ServiceCategory.objects.all()
    return {"cats": cats, "cat_selected": cat_selected}

@register.inclusion_tag('places/includes/tag_block.html')
def show_all_tags():
    return {"tags": TagService.objects.all()}


