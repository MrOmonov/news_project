from django.contrib import admin
from .models import (NewsModel, Category,
                     ContactModel, Comments)


# Register your models here.


@admin.register(NewsModel)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'status', 'category']
    list_display_links = ['id', 'title']
    prepopulated_fields = {'slug': ('title',), }
    list_filter = ['status', 'published_time']
    search_fields = ['title', 'body']
    date_hierarchy = 'published_time'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


admin.site.register(ContactModel)


def users_comments(object):
    return object.author.comments.count()


def short_news(object):
    return object.news.title[:70]


@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', short_news, 'body', 'created_time', 'active', users_comments]
    list_display_links = ['author', 'body']
    actions = ['make_active', 'make_disactive']

    def make_disactive(self, request, queryset):
        updated = queryset.update(active=False)
        self.message_user(request, f'{updated} malumot statusi uzgartirildi')

    def make_active(self, request, queryset):
        updated = queryset.update(active=True)
        self.message_user(request, f"{updated}ta commentlar active statusiga uzgartirildi")
