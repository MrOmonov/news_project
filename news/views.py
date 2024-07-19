from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, UpdateView, DeleteView, CreateView
from hitcount.models import HitCount
from hitcount.views import HitCountDetailView, HitCountMixin

from users.permissions import LoginSuperRequiredMixin
from .forms import ContactForm, ContactModelForm, CommentForm
from .models import NewsModel, ContactModel, Category, Comments


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
    template_name = 'news/single_page.html'
    context_object_name = 'news'
    slug_url_kwarg = 'news_slug'
    form_class = ContactModelForm
    success_url = reverse_lazy("self.get_object().get_absolute_url")

    def get_object(self, queryset=None):
        return get_object_or_404(NewsModel, slug=self.kwargs['news_slug'], status='PB')

    def post(self, request, *args, **kwargs):
        author = request.user
        news = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            form_success = form.save(commit=False)
            form_success.author = author
            form_success.news = news
            form_success.save()
            return redirect(news.get_absolute_url())
        else:
            context = self.get_context_data().update({'form': form})
            return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        news = self.get_object()
        hit_count = HitCount.objects.get_for_object(news)
        HitCountMixin.hit_count(self.request, hit_count)
        hit_count.refresh_from_db()

        context = {
            'hit_count': hit_count.hits,
            'form': CommentForm(),
            'comments': news.comments.all()
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


def single_page(request, news_slug):
    news = get_object_or_404(NewsModel, slug=news_slug)
    comments = news.comments.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.news_id = news.id
            comment.author = request.user
            comment.save()
            return redirect(news.get_absolute_url())
        else:
            forms.ValidationError('Formani to\'liq to\'ldiring')
    else:
        form = CommentForm()

    context = {
        'news': news,
        'title': news.title,
        'form': form,
        'comments': comments
    }
    return render(request, 'news/single_page.html', context)


def contactview(request):
    if request.method == 'POST':
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


@login_required
def errorview(request):
    context = {}
    return render(request, '404.html', context)


def aboutview(request):
    context = {}
    return render(request, 'about.html', context)


class ContactView(TemplateView):
    template_name = 'contact.html'

    def get(self, request, **kwargs):
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


class NewsUpdateView(UpdateView):
    model = NewsModel
    template_name = 'news/news_update.html'
    slug_url_kwarg = 'news_slug'
    fields = ('title', 'body', 'category', 'image', 'status')


class NewsDeleteView(DeleteView):
    model = NewsModel
    template_name = 'news/news_delete.html'
    slug_url_kwarg = 'news_slug'
    success_url = reverse_lazy('home_url')


class NewsCreateView(LoginSuperRequiredMixin, CreateView):
    model = NewsModel
    template_name = 'news/news_update.html'
    fields = ('title', 'body', 'category', 'image', 'status')
    success_url = reverse_lazy('home_url')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class SearchView(ListView):
    model = NewsModel
    template_name = 'news/filtered_news.html'
    context_object_name = 'list_news'

    def get_context_data(self, *, object_list=None, **kwargs):
        kwargs.update({'key': self.request.GET.get('q')})
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        search=self.request.GET.get('q', '')
        if search:
            news = NewsModel.objects.filter(Q(title__icontains=search)|Q(body__icontains=search))
            if not news:
                news=['Malumot topilmadi']
        else:
            news = NewsModel.objects.all()
        return news