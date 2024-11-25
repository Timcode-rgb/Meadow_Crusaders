from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('chara/<str:nom>/', views.chara_detail, name='chara_detail'),
    path('chara/<str:nom>/?<str:message>', views.chara_detail, name='chara_detail_mes'),
]