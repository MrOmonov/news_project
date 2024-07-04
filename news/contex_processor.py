from .models import NewsModel, Category

def latest_news(request):
    context={
        'latest_news': NewsModel.published.all()[:5],
        'categories' : Category.objects.filter(news_cat__gt=0).distinct()
    }
    return context