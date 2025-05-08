from django import forms
from django.core.exceptions import ValidationError
from .models import Service, OrderRequest
import datetime
import re

def validate_russian_chars(value):
    if not re.fullmatch(r'[А-Яа-яЁё0-9\s\-\.,/]+', value):
        raise ValidationError("Допустимы только русские буквы, цифры, пробел, дефис, точка, запятая и /.")

class OrderForm(forms.ModelForm):
    image = forms.ImageField(required=False, label="Изображение")  # Добавляем поле для изображения

    service = forms.ModelChoiceField(
        queryset=Service.objects.all(),
        empty_label="Услуга не выбрана",
        label="Тип услуги"
    )

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < datetime.date.today():
            raise ValidationError("Дата должна быть не раньше сегодняшней.")
        return date

    def clean_address(self):
        address = self.cleaned_data['address']
        validate_russian_chars(address)
        return address

    class Meta:
        model = OrderRequest
        fields = ['name', 'phone', 'address', 'date', 'service', 'comment', 'image']  # Добавляем поле 'image'
        labels = {
            'name': 'Ваше имя',
            'phone': 'Телефон',
            'address': 'Адрес',
            'date': 'Дата уборки',
            'comment': 'Комментарий',
            'image': 'Изображение'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-input'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'comment': forms.Textarea(attrs={'rows': 3, 'class': 'form-input'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-input'}),
        }
