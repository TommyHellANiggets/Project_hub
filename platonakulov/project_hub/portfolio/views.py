from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Fuel, Review
from .forms import ReviewForm

# Project Hub
def home(request):
    return render(request, 'home.html')

# Power Fuel
@login_required
def pf_profile(request):
    if request.method == 'POST':
        # Форма для смены пароля
        password_change_form = PasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)  # Обновление сессии пользователя
            return redirect('profile')  # Перенаправление на страницу профиля
    else:
        password_change_form = PasswordChangeForm(request.user)

    # Форма для смены электронной почты
    user_change_form = UserChangeForm(instance=request.user)

    context = {
        'password_change_form': password_change_form,
        'user_change_form': user_change_form,
    }
    return render(request, 'pf_profile.html', context)

@login_required
def pf_cart(request):
    return render(request, 'pf_cart.html')

def pf_home(request):
    fuels = Fuel.objects.all()
    reviews = Review.objects.all()[:3]  # Получение только трех отзывов
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pf-home')

    return render(request, 'pf_home.html', {'fuels': fuels, 'reviews': reviews, 'form': form})

def pf_catalog(request):
    return render(request, 'pf_catalog.html')

def pf_registration(request):
    return render(request, 'pf_registration.html')

def pf_authorisation(request):
    error_message = None

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('pf_home')
        else:
            error_message = "Неверный email или пароль. Пожалуйста, попробуйте снова."

    return render(request, 'pf_authorisation.html', {'error_message': error_message, 'user': request.user})

def pf_registration_view(request):
    show_notification = False

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        agree = request.POST.get('agree')

        if password != confirm_password:
            return render(request, 'pf_registration.html', {'show_notification': True})

        if not agree:
            return render(request, 'pf_registration.html', {'show_notification': True})

        # Создайте пользователя
        user = User.objects.create_user(username=name, email=email, password=password)
        user.save()

        # Аутентифицируйте и войдите в систему нового пользователя
        user = authenticate(request, username=name, password=password)
        if user is not None:
            login(request, user)
            # Перенаправьте пользователя на нужную страницу
            return redirect('pf_home')

    return render(request, 'pf_registration.html', {'show_notification': show_notification})


# Easy Goal 
def eg_home(request):
    return render(request, 'eg_home.html')

# Fears Of Alone 
def foa_home(request):
    return render(request, 'foa_home.html')

def foa_en_home(request):
    return render(request, 'foa_en_home.html')