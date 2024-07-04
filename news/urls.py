from django.urls import path

from news.views import (all_news, show_news,
                        NewsList, NewsDetail, homeview,
                        single_page, contactview, errorview,
                        aboutview, ContactView, category_news)


urlpatterns = [
    path('', NewsList.as_view(), name='home_url'),
    path('<slug:category_name>/' , category_news, name="show_category"),
    path('news/<slug:post_slug>/', single_page, name='show_news'),
    path('contact/', ContactView.as_view(), name='contact_page'),
    path('404page/', errorview, name='404_page'),
    path('about/', aboutview, name='about_page'),
    path('all_news/', NewsList.as_view(), name='all_news'),
    # path('news/<slug:post_slug>/', NewsDetail.as_view(), name='show_news')
]