from django.urls import path
from . import views

urlpatterns = [

    path("", views.lista, name="atendimento"),

    path(
        "novo/<int:agendamento_id>/",
        views.novo,
        name="atendimento_novo"
    ),

    path(
        "editar/<int:pk>/",
        views.editar,
        name="atendimento_editar"
    ),

    path(
        "excluir/<int:pk>/",
        views.excluir,
        name="atendimento_excluir"
    ),
path('atendimento/<int:pk>/imprimir/', views.atendimento_imprimir, name='atendimento_imprimir'),
]