from django.urls import path
from . import views

urlpatterns = [

    path("", views.lista, name="agenda"),

    path("novo/", views.novo, name="agenda_novo"),

    path("editar/<int:pk>/", views.editar, name="agenda_editar"),

    path("excluir/<int:pk>/", views.excluir, name="agenda_excluir"),

]