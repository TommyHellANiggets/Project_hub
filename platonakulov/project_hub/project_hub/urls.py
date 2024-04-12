from django.contrib import admin
from django.urls import path
from portfolio import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('pf-home/', views.pf_home, name='pf-home'),
    path('pf-registration/', views.pf_registration, name='pf-registration'),
    path('pf-authorisation/', views.pf_authorisation, name='pf-authorisation'),
    path('pf-cart/', views.pf_cart, name='pf-cart'),
    path('pf-catalog/', views.pf_catalog, name='pf-catalog'),
    path('pf-profile/', views.pf_profile, name='pf-profile'),
    path('search-suggestions/', views.search_suggestions, name='search_suggestions'),
    path('add-to-cart/<slug:slug>/', views.add_to_cart, name='add-to-cart'),
    path('get-cart/', views.get_cart, name='get-cart'),
    path('fuels/<slug:slug>/', views.fuel_detail, name='fuel-detail'),
    path('eg-home/', views.eg_home, name='eg-home'),
    path('foa-home/', views.foa_home, name='foa-home'),
    path('foa-en-home/', views.foa_en_home, name='foa-en-home'),
]

handler404 = 'portfolio.views.error_404'
