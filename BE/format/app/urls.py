from django.urls import path
from . import views

urlpatterns = [
    path('cargar/', views.cargar_documento, name='cargar_documento'),
    path('ver/<int:documento_id>/', views.ver_documento, name='ver_documento'),
    path('extraer/<int:documento_id>/', views.extraer_texto, name='extraer_texto'),
    path('resultado/<int:documento_id>/', views.resultado_documento, name='resultado_documento'),
]
