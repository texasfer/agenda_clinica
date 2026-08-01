from django.urls import path

from . import views

urlpatterns=[

    path("",views.lista,name="clientes"),

    path("novo/",views.novo,name="cliente_novo"),

    path("editar/<int:pk>/",views.editar,name="cliente_editar"),

    path("excluir/<int:pk>/",views.excluir,name="cliente_excluir"),

]