from django.contrib import admin
from .models import Service, ServiceCategory
from django.contrib import messages


class PriceRangeFilter(admin.SimpleListFilter):
    title = 'Ценовой диапазон'
    parameter_name = 'price_range'

    def lookups(self, request, model_admin):
        return [
            ('low', 'До 5000 руб.'),
            ('mid', '5000–15000 руб.'),
            ('high', 'Свыше 15000 руб.')
        ]

    def queryset(self, request, queryset):
        if self.value() == 'low':
            return queryset.filter(price__lt=5000)
        elif self.value() == 'mid':
            return queryset.filter(price__gte=5000, price__lte=15000)
        elif self.value() == 'high':
            return queryset.filter(price__gt=15000)

class ServiceAdmin(admin.ModelAdmin):
    fields = ['name', 'slug', 'description', 'price', 'category', 'is_published', 'tags', 'image']
    list_display = ('id', 'name', 'price','is_published', 'category', 'brief_info')
    list_display_links = ('id', 'name')
    ordering = ['id']
    list_editable = ['price', 'is_published']
    list_per_page = 10
    actions = ['set_published', 'set_draft']
    search_fields = ['name', 'category__name']
    list_filter = [PriceRangeFilter, 'category__name', 'is_published']
    filter_horizontal = ['tags']



    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=True)
        self.message_user(request, f"Опубликовано: {count} записи(ей).")

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=False)
        self.message_user(
            request,
            f"Снято с публикации: {count} записи(ей).",
            messages.WARNING
        )

    @admin.display(description="Краткое описание", ordering='description')
    def brief_info(self, obj):
        return f"Описание: {len(obj.description)} символов"

admin.site.register(Service, ServiceAdmin)
admin.site.site_header = "Панель управления BossClean"
admin.site.index_title = "Управление услугами клининга"

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    ordering = ['id']


admin.site.register(ServiceCategory, CategoryAdmin)

# Register your models here.
