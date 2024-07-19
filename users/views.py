from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from users.forms import (LoginForm, RegisterForm,
                         RegisterBaseForm, UserEditForm,
                         ProfileEditForm)
from users.models import Profile
from django.contrib.auth.decorators import login_required, user_passes_test


def profile_view(request):
    user = request.user
    context = {
        'user': user,
    }
    try:
        profile = Profile.objects.get(user=user)
        context['profile'] = profile
    except:
        profile = None
    return render(request, 'users/profile.html', context=context)


# Create your views h
# ere.
def loginView(request):
    context = {
        'title': 'Saytga kirish uchun malumotlaringizni kiriting',
        'form': LoginForm()
    }
    if request.method == 'POST':

        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request,
                                username=data['username'],
                                password=data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home_url')
            return HttpResponse('Bunaqa user topilmadi')
    else:
        return render(request, 'users/login.html', context=context)


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            print(form.cleaned_data['password1'])
            user.save()
            Profile.objects.create(user)
            return render(request, 'users/registration_done.html', {})
        else:
            context = {
                'form': form
            }
            return render(request, 'users/registration.html', context)
    else:
        context = {
            'form': RegisterForm()
        }
        return render(request, 'users/registration.html', context)


class RegisterView(CreateView):
    """Registratsiya vaqtida Profileniham yaratadigan View"""
    form_class = RegisterBaseForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('login_user')

    def form_valid(self, form):
        response = super().form_valid(form)  #formani bazaga saqlash
        Profile.objects.create(user=self.object)  #Profile obyektini yaratish
        return response


def profile_edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('home_url')
        # else:
        #     raise ValidationError('Hamma ma\'lumotlar to\'ldirilganligiga ishonch xosil qiling')

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'users/profile_edit.html', context=context)


@user_passes_test(lambda i: i.is_superuser)
@login_required
def admin_panel(request):
    admins = User.objects.filter(is_superuser=True, is_active=True)
    users = User.objects.filter(is_superuser=False, is_active=True)

    context = {
        'admins': admins,
        "users": users
    }
    return render(request, 'users/admin_panel.html', context=context)
