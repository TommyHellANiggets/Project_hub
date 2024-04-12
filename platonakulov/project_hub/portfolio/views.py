from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Review, Fuel, CartItem
from .forms import ReviewForm, SearchForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse


from django.utils.crypto import get_random_string

from django.utils.text import slugify
from django.utils.crypto import get_random_string

def generate_unique_slug(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.name)

    queryset = Fuel.objects.filter(slug=slug).exclude(id=instance.id)
    if queryset.exists():
        new_slug = f"{slug}-{get_random_string(length=4)}"
        return generate_unique_slug(instance, new_slug=new_slug)
    return slug

def get_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    cart_data = {'cart': {}}

    for item in cart_items:
        cart_data['cart'][item.id] = {
            'name': item.fuel.name,
            'price': float(item.fuel.price),
            'photo_url': item.fuel.photo_url.url if item.fuel.photo_url else None,
        }

    return JsonResponse(cart_data)

def add_to_cart(request, slug):
    fuel = get_object_or_404(Fuel, slug=slug)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, fuel=fuel)

    if created:
        return JsonResponse({'message': 'Товар успешно добавлен в корзину.'})
    else:
        return JsonResponse({'message': 'Товар уже находится в корзине.'})

# Остальные представления остаются без изменений



def fuel_detail(request, slug):
    fuel = get_object_or_404(Fuel, slug=slug)
    return render(request, 'fuel_detail.html', {'fuel': fuel})


def error_404(request, exception):
    return render(request, 'pf_404.html', status=404)

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
    fuels = Fuel.objects.all()[:12]  # Получение максимум 12 объектов Fuel
    reviews = Review.objects.all()[:3]  # Получение только трех отзывов
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pf-home')

    return render(request, 'pf_home.html', {'fuels': fuels, 'reviews': reviews, 'form': form})


def search_suggestions(request):
    query = request.GET.get('query')
    if query:
        fuels = Fuel.objects.filter(name__icontains=query)[:5]  # Получить первые 5 объектов Fuel, содержащих введенный запрос
        suggestions = [fuel.name for fuel in fuels]  # Получить список предложенных запросов
        return JsonResponse({'suggestions': suggestions})
    else:
        return JsonResponse({'suggestions': []})

def pf_catalog(request):
    fuels_list = Fuel.objects.all()
    query = request.GET.get('search')
    if query:
        fuels_list = fuels_list.filter(name__icontains=query)

    paginator = Paginator(fuels_list, 12)

    page = request.GET.get('page')
    try:
        fuels = paginator.page(page)
    except PageNotAnInteger:
        fuels = paginator.page(1)
    except EmptyPage:
        fuels = paginator.page(paginator.num_pages)

    reviews = Review.objects.all()[:3]
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pf-home')

    return render(request, 'pf_catalog.html', {'fuels': fuels, 'reviews': reviews, 'form': form, 'search_form': SearchForm()})






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

