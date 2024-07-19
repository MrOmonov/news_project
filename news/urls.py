from django.urls import path
from users.views import admin_panel
from news.views import (all_news, show_news,
                        NewsList, NewsDetail, homeview,
                        single_page, contactview, errorview,
                        aboutview, ContactView, category_news,
                        NewsUpdateView, NewsDeleteView,
                        NewsCreateView,SearchView)


urlpatterns = [
    path('', NewsList.as_view(), name='home_url'),
    path('admin_panel/', admin_panel, name="admin_panel"),
    path('news/create', NewsCreateView.as_view(), name='news_create'),
    path('edit/<slug:news_slug>/', NewsUpdateView.as_view(), name="update_news"),
    path('delete/<slug:news_slug>/', NewsDeleteView.as_view(), name="delete_news"),
    # path('news/<slug:news_slug>/', single_page, name='show_news'),
    path('news/<slug:news_slug>/', NewsDetail.as_view(), name='show_news'),
    path('filtered_news/', SearchView.as_view(), name='filtered_news'),
    path('contact/', ContactView.as_view(), name='contact_page'),
    path('404page/', errorview, name='404_page'),
    path('about/', aboutview, name='about_page'),
    path('all_news/', NewsList.as_view(), name='all_news'),
    path('<slug:category_name>/' , category_news, name="show_category"),



]