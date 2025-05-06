from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import render_to_string


'''
menu = ["О компании", "Услуги", "Контакты", "Вход"]

class Info:
    def __init__(self, email, phone):
        self.email = email
        self.phone = phone
'''

menu = [{'title': "Главная", 'url_name': 'home'},
        {'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить услугу", 'url_name':'add_page'},
        {'title': "Обратная связь", 'url_name':'contact'},
        {'title': "Войти", 'url_name': 'login'}
]


services = [
    {'id': 1, 'title': 'Генеральная уборка', 'description': 'Полная уборка квартиры', 'is_available': True},
    {'id': 2, 'title': 'Мойка окон', 'description': 'Чистим окна без разводов', 'is_available': False},
    {'id': 3, 'title': 'Уборка после ремонта', 'description': 'Удалим строительную пыль', 'is_available': True},
]

services_db = [
    {'id': 1, 'name': 'Уборка однокомнатной квартиры'},
    {'id': 2, 'name': 'Уборка двухкомнатной квартиры'},
    {'id': 3, 'name': 'Уборка трехкомнатной квартиры'},
    {'id': 4, 'name': 'Уборка квартиры с более чем 3 комнатами'}
]

# Create your views here.
def index(request):
    return HttpResponse("Это страница приложения places.")

def categories(request, so_id):
    return HttpResponse(f"<h1>Категории</h1><p>id: {so_id}</p>")

def categoriesBySlug(request, so_slug):
    return HttpResponse(f"<h1>Категории</h1><p>slug: {so_slug}</p>")

'''
def categoriesBySlug(request, so_slug):
    if request.GET:
        print("request.GET")
    return HttpResponse(f"<h1>Категории</h1><p>slug: {so_slug}</p>")

def categoriesBySlug(request, so_slug):
    if request.POST:
        print("request.POST")
    return HttpResponse(f"<h1>Категории</h1><p>slug: {so_slug}</p>")
'''

def archive(request, year):
    if (year > 2025):
        uri = reverse('so_slug', args=('hotels',))
        return HttpResponseRedirect('/')
    return HttpResponse(f"<h1>Архив по годам</h1><p>Год: {year}</p>")

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")

def index(request):

    context = {
        'title': 'Главная',
        'services': services,
        'menu': menu,
        'active_page': 'home'
    }
    return render(request, 'places/index.html', context)


def about(request):
    return render(request, 'places/about.html', {'title': 'О компании', 'menu': menu, 'active_page': 'about'})

def show_service(request, service_id):
    return HttpResponse(f"Детали услуги с ID = {service_id}")

def addpage(request):
    return render(request, 'places/addpage.html', context = {'menu': menu, 'active_page': 'add_page'})
def contact(request):
    return render(request, 'places/contact.html', context = {'menu': menu, 'active_page': 'contact'})
def login(request):
    return render(request, 'places/login.html', context = {'menu': menu, 'active_page': 'login'})



