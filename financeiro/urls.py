from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.lista,
        name="financeiro"
    ),

    path(
        "baixar/<int:pk>/",
        views.baixar,
        name="financeiro_baixar"
    ),

    path(
        "estornar/<int:pk>/",
        views.estornar,
        name="financeiro_estornar"
    ),

    path(
        "excluir/<int:pk>/",
        views.excluir,
        name="financeiro_excluir"
    ),

]