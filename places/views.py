from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib import messages
from .forms import OrderForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView
from django.shortcuts import render
from .gpt_api import ask_yandex_gpt, ask_yandex_gpt_with_history
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .gpt_api import ask_yandex_gpt
from places.models import Service, ServiceCategory, TagService, OrderRequest

'''
menu = ["О компании", "Услуги", "Контакты", "Вход"]

class Info:
    def __init__(self, email, phone):
        self.email = email
        self.phone = phone
'''

menu = [{'title': "Главная", 'url_name': 'home'},
        {'title': "О сайте", 'url_name': 'about'},
        {'title': "Оставить заявку", 'url_name':'add_request'},
        {'title': "Обратная связь", 'url_name':'contact'},
]


services = [
    {'id': 1, 'title': 'Общие услуги', 'description': 'Общие услуги', 'is_available': True},
    {'id': 2, 'title': 'Домашняя уборка', 'description': 'Домашняя уборка', 'is_available': True},
    {'id': 3, 'title': 'Уборка офисных помещений', 'description': 'Уборка офисных помещений', 'is_available': True},
]

services_db = [
    {'id': 'slug-1', 'name': 'Уборка однокомнатной квартиры'},
    {'id': 'slug-2', 'name': 'Уборка двухкомнатной квартиры'},
    {'id': 'slug-3', 'name': 'Уборка трехкомнатной квартиры'},
    {'id': 'slug-4', 'name': 'Уборка квартиры с более чем 3 комнатами'}
]

# Create your views here.
def in_group(group_name):
    def check(user):
        return user.is_authenticated and user.groups.filter(name=group_name).exists()
    return check


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
    services = Service.objects.filter(is_published=True)

    context = {
        'title': 'Главная',
        'posts': services,
        'cat_selected': 0,
        'active_page': 'home'
    }
    return render(request, 'places/index.html', context)


def about(request):
    return render(request, 'places/about.html', {'title': 'О компании', 'active_page': 'about'})

def show_service(request, service_slug):
    service = get_object_or_404(Service, slug=service_slug)

    data = {
        'title': service.name,
        'service': service,
        'active_page': 'home'
    }
    return render(request, 'places/service.html', data)

@login_required
def add_request(request):
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            return redirect('order_success', order_id=order.id)
    else:
        form = OrderForm()

    return render(request, 'places/add_request.html', {'form': form, 'active_page': 'add_request'})


#@permission_required('places.view_orderrequest', raise_exception=True)
def order_success(request, order_id):
    order = get_object_or_404(OrderRequest, id=order_id)
    return render(request, 'places/order_success.html', {'order': order})

def cancel_order(request, order_id):
    order = get_object_or_404(OrderRequest, id=order_id)
    if request.method == 'POST':
        order.delete()
        return redirect('home')
    return render(request, 'places/cancel_order.html', {'order': order})

@login_required
@user_passes_test(in_group('Admin'))
def contact(request):
    return render(request, 'places/contact.html', context = { 'active_page': 'contact'})
def login(request):
    return render(request, 'places/login.html', context = { 'active_page': 'login'})

def show_category(request, cat_slug):
    category = get_object_or_404(ServiceCategory, slug=cat_slug)
    posts = Service.published.filter(category=category)
    context = {
        'title': f'Рубрика: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
    }
    return render(request, 'places/index.html', context=context)

def show_tag_services(request, tag_slug):
    tag = get_object_or_404(TagService, slug=tag_slug)
    posts = tag.services.filter(is_published=True)

    context = {
        'title': f'Тег: {tag.tag}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
        'tag_selected': tag.slug,
    }
    return render(request, 'places/index.html', context=context)

class MyOrdersView(LoginRequiredMixin, ListView):
#class MyOrdersView(LoginRequiredMixin, '''PermissionRequiredMixin''', ListView):
    model = OrderRequest
    template_name = 'places/my_orders.html'
    context_object_name = 'orders'
    login_url = 'users:login'
    #permission_required = 'places.my_orders.html'

    def get_queryset(self):
        return OrderRequest.objects.filter(user=self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'my_orders'
        return context

def gpt_chat(request):
    response_text = ""
    if request.method == "POST":
        user_prompt = request.POST.get("prompt")
        response_text = ask_yandex_gpt(user_prompt)

    return render(request, "places/gpt_chat.html", {"response": response_text})


@csrf_exempt
def gpt_chat_ajax(request):
    if request.method == "POST":
        data = json.loads(request.body)
        messages = data.get("messages", [])
        response_text = ask_yandex_gpt_with_history(messages)
        return JsonResponse({"response": response_text})
    return JsonResponse({"error": "Invalid request"}, status=400)

