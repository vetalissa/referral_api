import random
from time import sleep

from django.contrib.auth import logout
from django.shortcuts import redirect, render

from .forms import CodeForm, PhoneNumberForm
from .models import User


def login(request):
    """ Вход, ввод номера телефона и звонок(генерация кода) для входа. """
    if request.method == 'POST':
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            phone_number = form.data['phone_number']

            # Имитация вызова
            sleep(2)
            code = str(random.randint(1000, 9999))

            # Сохраняем временные данные
            request.session['verify_code'] = code
            request.session['phone_number'] = phone_number

            return redirect('users:login_authenticate')
    else:
        form = PhoneNumberForm()

    return render(request, 'users/send_code.html', {'form': form})


def login_authenticate(request):
    """ Продолжение входа, ввод 4х значного кода. """
    if request.method == 'POST':
        form = CodeForm(request.POST)
        if form.is_valid():
            code = form.data['code']

            # Проверка, что пользователь ввел верный код
            if code == request.session.get('verify_code'):
                phone_number = request.session.get('phone_number')

                # Если пользователя нет, создаем его
                User.objects.get_or_create(phone_number=phone_number)

                # Сообщаем, что мы прошли аутентификацию
                request.session['user_authenticate'] = True

                return redirect('users:profile')  # Переход к профилю пользователя
    else:
        form = CodeForm()

    context = {'form': form, 'code': request.session.get('verify_code')}
    return render(request, 'users/verify_code.html', context)


def user_profile(request):
    """  Профиль пользователя. """
    # Проверка, что пользователь прошел аутентификацию
    if request.session.get('user_authenticate'):
        user = User.objects.get(phone_number=request.session['phone_number'])

        if request.method == 'POST':
            invite_code = request.POST.get('invite_code')

            if not user.activate_invite_code:
                if User.objects.filter(user_invite_code=invite_code).exists():
                    user.activate_invite_code = invite_code
                    user.save()
                    message = "Инвайт-код успешно активирован"
                else:
                    message = "Инвайт-код не найден..."
            else:
                message = f"Вы уже активировали инвайт-код: {user.activate_invite_code}"

            context = {'user': user, 'message': message}

            return render(request, 'users/user_profile.html', context)

        # инвайт код пользователя
        invite_code = user.user_invite_code

        # Проверка на активированный инвайт-код
        if user.activate_invite_code:
            activ_invite_code = user.activate_invite_code
        else:
            activ_invite_code = False

        # Список пользователей, которые использовали инвайт-код текущего пользователя
        # invited_users = User.objects.filter(activate_invite_code=user.user_invite_code)
        invited_users = user.get_who_activate_my_code()

        context = {'user': user, 'invited_users': invited_users,
                   'invite_code': invite_code, 'activ_invite_code': activ_invite_code}

        return render(request, 'users/user_profile.html', context)
    # При попытке зайти на профиль, без номера и ввода кода
    return redirect('users:login')


def logout_view(request):
    """ Выходим, стираем сессии. """
    logout(request)
    return redirect('users:login')

