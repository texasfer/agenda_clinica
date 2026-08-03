from django.urls import path
from . import views

urlpatterns = [
    # Lista
    path("", views.lista, name="atendimento"),

    # Novo Atendimento sem agendamento prévio
    path("novo/", views.criar_atendimento, name="atendimento_novo"),

    # Novo Atendimento vinculado a um Agendamento da Agenda
    path("novo/<int:agendamento_id>/", views.criar_atendimento, name="atendimento_novo_agendamento"),

    # Edição e Exclusão
    path("editar/<int:pk>/", views.editar, name="atendimento_editar"),
    path("excluir/<int:pk>/", views.excluir, name="atendimento_excluir"),

    # Impressão
    path("<int:pk>/imprimir/", views.atendimento_imprimir, name="atendimento_imprimir"),
]