from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('registrera/', views.registrera, name='registrera'),
    path('loggain/',auth_views.LoginView.as_view(template_name='listor/loggain.html'),name='loggain'),
    path('loggaut/',auth_views.LogoutView.as_view(),name='loggaut'),

    path('', views.AllaListor.as_view(), name='listor-hem'),
    path('lista/<int:pk>/', views.EnLista.as_view(), name='lista-sida'),
    path('lista/<int:pk>/uppdatera/', views.UppdateraLista.as_view(), name='lista-uppdatera'),
    path('lista/<int:pk>/radera/', views.RaderaLista.as_view(), name='lista-radera'),
    path('lista/ny/', views.SkapaLista.as_view(), name='lista-ny'),
    
    path('artikel/<int:pk>/uppdatera/', views.UppdateraArtikel.as_view(), name='artikel-uppdatera'),
    path('artikel/<int:pk>/radera/', views.RaderaArtikel.as_view(), name='artikel-radera'),
    path('artikel/<int:l_pk>/ny/', views.SkapaArtikel.as_view(), name='artikel-ny'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)