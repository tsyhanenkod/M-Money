from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views import View
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .forms import *
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DeleteView
from django.urls import reverse_lazy

class LoginView(View):
    def get(self, request):
        form = LoginForm()

        initial_data = {'email': '', 'password': ''}
        form = LoginForm(initial=initial_data)

        context = {
            'form': form,
        }
        return render(request, 'loging/login.html', context)

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error('password', 'Invalid email or password')

        context = {
            'form': form,
        }
        return render(request, 'loging/login.html', context)




class SignupView(View):
    def get(self, request):
        form = SignupForm()

        initial_data = {
            'first_name': '',
            'last_name': '',
            'email': '',
            'password': '',
            'password_confirmation': '',
        }
        form = SignupForm(initial=initial_data)

        context = {
            'form': form,
        }
        return render(request, 'loging/signup.html', context)

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password_confirmation = form.cleaned_data['password_confirmation']

            # Проверка электронной почты
            if User.objects.filter(username=email).exists():
                form.add_error('email', 'Email already exists')

            # Проверка пароля
            if password != password_confirmation:
                form.add_error('password_confirmation', 'Passwords do not match')

            if form.errors:
                error_message = 'Form has errors'
                context = {
                    'form': form,
                    'error_message': error_message,
                }

                if 'password_confirmation' in form.errors:
                    form.fields['password_confirmation'].widget.attrs['value'] = ''
                else:
                    form.fields['password_confirmation'].widget.attrs['value'] = request.POST.get(
                        'password_confirmation', '')

                return render(request, 'loging/signup.html', context)

            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            # Аутентификация и вход пользователя в систему
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)

            return redirect('home')

        context = {
            'form': form,
            'error_message': 'Form has errors',
        }

        return render(request, 'loging/signup.html', context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

    def post(self, request):
        logout(request)
        return redirect('login')


class ProfileView(View):
    def get(self, request):

        context = {

        }
        return render(request, 'loging/profile.html', context)


@method_decorator(login_required, name='dispatch')
class ProfileEditView(View):
    def get(self, request):
        user = request.user
        form = ChangePasswordForm()
        form2 = ChangeUserData(initial={
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        })
        context = {
            'form': form,
            'form2': form2,
        }
        return render(request, 'loging/profile_edit.html', context)

    def post(self, request):
        if 'change_password' in request.POST:
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                current_password = form.cleaned_data['current_password']
                new_password = form.cleaned_data['new_password']
                new_password_confirmation = form.cleaned_data['new_password_confirmation']

                user = request.user

                if not user.check_password(current_password):
                    form.add_error('current_password', 'Неверный текущий пароль.')
                elif new_password != new_password_confirmation:
                    form.add_error('new_password_confirmation', 'Подтверждение нового пароля не совпадает.')
                else:
                    user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request, user)
                    return redirect('profile')
            else:
                if 'current_password' in form.errors:
                    form.add_error('current_password', form.errors['current_password'])
                if 'new_password' in form.errors:
                    form.add_error('new_password', form.errors['new_password'])
                if 'new_password_confirmation' in form.errors:
                    form.add_error('new_password_confirmation', form.errors['new_password_confirmation'])

                context = {
                    'form': form,
                    'form2': ChangeUserData(initial={
                        'email': request.user.email,
                        'first_name': request.user.first_name,
                        'last_name': request.user.last_name,
                    }),
                }
                return render(request, 'loging/profile_edit.html', context)

        elif 'change_user_data' in request.POST:
            form2 = ChangeUserData(request.POST)

            if form2.is_valid():
                user = request.user
                user.email = form2.cleaned_data['email']
                user.first_name = form2.cleaned_data['first_name']
                user.last_name = form2.cleaned_data['last_name']
                user.save()
                messages.success(request, 'Данные пользователя успешно изменены.')
            else:
                messages.error(request, 'Произошла ошибка при изменении данных пользователя.')

            return redirect('profile')

        user = request.user
        form = ChangePasswordForm()
        form2 = ChangeUserData(initial={
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        })
        context = {
            'form': form,
            'form2': form2,
        }
        return render(request, 'loging/profile_edit.html', context)


class DeleteProfile(DeleteView):
    model = User
    success_url = reverse_lazy('login')

    def get_object(self, queryset=None):
        user_id = self.kwargs.get('user_id')
        return get_object_or_404(User, id=user_id)