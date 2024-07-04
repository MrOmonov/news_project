from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView

from .forms import ContactForm
from .models import NewsModel, ContactModel, Category


# Create your views here.
def all_news(request):
    news_list = NewsModel.published.all()
    context = {
        'title': "Bosh saxifa",
        'news_list': news_list
    }
    return render(request, 'news/home.html', context=context)


def show_news(request, post_slug):
    news = get_object_or_404(NewsModel, slug=post_slug)
    context = {
        'title': news.title,
        'news': news
    }
    return render(request, 'news/show_news.html', context=context)


def homeview(request):
    news = NewsModel.published.all()[:5]
    category = Category.objects.filter(news_cat__gt=0).distinct()
    main_sport = NewsModel.published.filter(category__name='Sport')[0]
    sport_list = NewsModel.published.filter(category__name='Sport')[1:6]
    context = {
        'news_list': news,
        'categories': category,
        'main_sport': main_sport,
        'sport_list': sport_list,
        'title': 'Bosh saxifa'
    }
    return render(request, 'index.html', context=context)


class NewsList(ListView):
    model = NewsModel
    template_name = 'index.html'
    context_object_name = 'news_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['categories'] = Category.objects.filter(news_cat__gt=0).distinct()
        context['sport_list'] = NewsModel.published.filter(category__name='Sport')[:6]
        context['texnology_list'] = NewsModel.published.filter(category__name='Texnologiyalar')[:6]
        context['ijtimoiy_list'] = NewsModel.published.filter(category__name='Ijtimoiy')[:6]
        context['siyosiy_list'] = NewsModel.published.filter(category__name='Siyosat')[:6]
        return context

    def get_queryset(self):
        return NewsModel.published.all()[:5]


class NewsDetail(DetailView):
    model = NewsModel
    template_name = 'news/show_news.html'
    context_object_name = 'news'

    # slug_url_kwarg = 'post_slug'

    def get_object(self, queryset=None):
        return get_object_or_404(NewsModel, slug=self.kwargs['post_slug'], status='PB')


def single_page(request, post_slug):
    news = get_object_or_404(NewsModel, slug=post_slug)
    context = {
        'news': news,
        'title': news.title
    }
    return render(request, 'news/single_page.html', context)


def contactview(request):
    if request.method=='POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            ContactModel.objects.create(**form.cleaned_data)
            return redirect('home_url')
    else:
        form = ContactForm()
    context = {
        'title': 'Biz bilan aloqa',
        'form': form,
        'text': 'Biz bilan bog\'lanish qilish uchun sahifa. Muammoyingizni iloji boricha tezroq hal qilishimiz uchun ma\'lumotlaringizni to\'liq kiriting'
    }
    return render(request, 'contact.html', context)


def errorview(request):
    context = {}
    return render(request, '404.html', context)


def aboutview(request):
    context = {}
    return render(request, 'about.html', context)


class ContactView(TemplateView):
    template_name = 'contact.html'

    def get(self, request):
        form = ContactForm()
        context = {
        'title': 'Biz bilan aloqa',
        'form': form,
        'text': 'Biz bilan bog\'lanish qilish uchun sahifa. Muammoyingizni iloji boricha tezroq hal qilishimiz uchun ma\'lumotlaringizni to\'liq kiriting'
    }
        return render(request, 'contact.html', context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactModel.objects.create(**form.cleaned_data)
            return redirect('home_url')
        context = {
            'title': 'Biz bilan aloqa',
            'form': form,
            'text': 'Biz bilan bog\'lanish qilish uchun sahifa. Muammoyingizni iloji boricha tezroq hal qilishimiz uchun ma\'lumotlaringizni to\'liq kiriting'
        }
        return render(request, 'contact.html', context)


def category_news(request, category_name):
    category = Category.objects.filter(name=category_name)[0]
    news = NewsModel.published.filter(category=category)
    context = {
        'category': category,
        'news_list': news
    }
    return render(request, 'news/categories.html', context)