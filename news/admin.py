from django.contrib import admin
from .models import NewsModel, Category, ContactModel


# Register your models here.


@admin.register(NewsModel)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'status', 'category']
    list_display_links = ['id', 'title']
    prepopulated_fields = {'slug': ('title',),}
    list_filter = ['status', 'published_time']
    search_fields = ['title', 'body']
    date_hierarchy = 'published_time'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

admin.site.register(ContactModel)
