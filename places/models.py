from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Service.Status.PUBLISHED)

class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название категории')
    slug = models.SlugField(unique=True, verbose_name='URL')

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    def __str__(self):
        return self.name

class TagService(models.Model):
    tag = models.CharField(max_length=100, db_index=True, verbose_name="Название тега")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})

class Service(models.Model):

    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    name = models.CharField(max_length=255, verbose_name="Название услуги")
    slug = models.SlugField(max_length=255, unique=False, db_index=True, verbose_name="URL", blank=True)
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена")
    is_published = models.BooleanField(
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name="Статус публикации"
    )
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, default='1', verbose_name='Категория', related_name='posts')
    tags = models.ManyToManyField(TagService, blank=True, related_name='services', verbose_name="Теги")
    image = models.ImageField(upload_to='services/', blank=True, null=True)

    objects = models.Manager()         # стандартный менеджер
    published = PublishedManager()    # пользовательский менеджер

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('service_detail', kwargs={'service_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-price']
        indexes = [
            models.Index(fields=['-price']),
        ]



