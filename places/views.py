from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse


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