from django.contrib import admin
from django.urls import path
from portfolio import views

# Project Hub
urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
# Power Fuel
    path('pf-home/', views.pf_home, name='pf-home'),  # URL для главной страницы
    path('pf-registration/', views.pf_registration, name='pf-registration'),  # URL для страницы регистрации
    path('pf-authorisation/', views.pf_authorisation, name='pf-authorisation'),  # URL для страницы авторизации
    path('pf-cart/', views.pf_cart, name='pf-cart'),  # URL для страницы корзины
    path('pf-catalog/', views.pf_catalog, name='pf-catalog'),  # URL для страницы каталога
    path('pf-profile/', views.pf_profile, name='pf-profile'),  # URL для страницы профиля
# индивидуальный url
    path('fuels/<int:fuel_id>/', views.fuel_detail, name='fuel-detail'),
# Easy Goal
    path('eg-home/', views.eg_home, name='eg-home'),  
# Smart Skill

# Fears Of Alone
    path('foa-home/', views.foa_home, name='foa-home'),  
    path('foa-en-home/', views.foa_en_home, name='foa-en-home'),  
]