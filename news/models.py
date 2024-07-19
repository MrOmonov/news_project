from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django.utils import timezone
import transliterate
from hitcount.models import HitCount, HitCountMixin
from slugify import slugify
from .managers import Publishedmanager


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=250)

    class Meta:
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'

    def __str__(self):
        return self.name


class NewsModel(models.Model):
    class Status(models.TextChoices):
        Draft = 'DF', 'Draft'
        Published = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True, db_index=True, null=True, blank=True)
    body = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Kategoriya', related_name='news_cat')
    image = models.ImageField(upload_to='news/images')
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    published_time = models.DateTimeField(default=timezone.now)
    status = models.CharField(choices=Status.choices, default=Status.Draft, max_length=2)
    author = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)

    objects = models.Manager()
    published = Publishedmanager()

    class Meta:
        ordering = ['-published_time']
        verbose_name = 'Yangilik'
        verbose_name_plural = 'Yangiliklar'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # print(slugify(self.title))
        # self.slug = transliterate.slugify(self.title)
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        # print('All saved', self.slug)

    def get_absolute_url(self):
        return reverse("show_news", kwargs={'news_slug': self.slug})


class ContactModel(models.Model):
    name = models.CharField(max_length=150, verbose_name='FIO')
    email = models.EmailField(verbose_name='E-mail')
    message = models.TextField(verbose_name='Matn')

    def __str__(self):
        return self.email


class Comments(models.Model):
    news = models.ForeignKey(NewsModel,
                             on_delete=models.CASCADE,
                             related_name='comments')
    author = models.ForeignKey(User,
                               related_name='comments',
                               on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_time']

    def __str__(self):
        return f"Bu komment:{self.body}.Muallif: {self.author} "
