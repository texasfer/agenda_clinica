from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista, name='financeiro'),
    path('novo/', views.salvar_lancamento, name='financeiro_criar'),
    path('editar/<int:pk>/', views.salvar_lancamento, name='financeiro_editar'),
    path('baixar/<int:pk>/', views.baixar, name='financeiro_baixar'),
    path('estornar/<int:pk>/', views.estornar, name='financeiro_estornar'),
    path('excluir/<int:pk>/', views.excluir, name='financeiro_excluir'),
    path('', views.dashboard_financeiro, name='financeiro'),
]