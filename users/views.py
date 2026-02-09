from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView
from .forms import LoginUserForm, ProfileUserForm, UserPasswordChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from .forms import RegisterUserForm
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.conf import settings

User = get_user_model()

class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = "users/password_change_form.html"
    success_url = reverse_lazy("users:password_change_done")
    extra_context = {'title': "Изменение пароля"}

class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': "Профиль пользователя", 'default_image': settings.DEFAULT_USER_IMAGE}

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Профиль успешно обновлён.")
        return super().form_valid(form)


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    extra_context = {'title': "Регистрация"}

    def form_valid(self, form):
        user = form.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(self.request, user)
        messages.success(self.request, 'Вы успешно зарегистрировались на сайте!')
        return redirect(self.success_url)


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'
    extra_context = {'title': "Авторизация"}

    def get_success_url(self):
        return self.request.GET.get('next', reverse_lazy('home'))


'''
def login_user(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user and user.is_active:
                login(request, user)
                return redirect('home')
    else:
        form = LoginUserForm()
    return render(request, 'users/login.html', {'form': form, 'active_page': 'users.login'})

def logout_user(request):
    logout(request)
    return redirect('users:login')
'''

'''
def register(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'users/register_done.html')
    else:
        form = RegisterUserForm()
    return render(request, 'users/register.html', {'form': form})
'''

'''
def register(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'users/register_done.html')
    else:
        form = RegisterUserForm()
    return render(request, 'users/register.html', {'form': form})
'''