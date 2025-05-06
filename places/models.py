import reverse
from django.db import models
from django.utils.text import slugify


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Service.Status.PUBLISHED)

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
    image = models.ImageField(upload_to='services/', blank=True, null=True)

    objects = models.Manager()         # стандартный менеджер
    published = PublishedManager()    # пользовательский менеджер

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('service', kwargs={'service_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-price']
        indexes = [
            models.Index(fields=['-price']),
        ]

