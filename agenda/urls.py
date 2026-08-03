from django.urls import path
from . import views

urlpatterns = [

    path("", views.lista, name="agenda"),

    path("novo/", views.novo, name="agenda_novo"),

    path("editar/<int:pk>/", views.editar, name="agenda_editar"),

    path("excluir/<int:pk>/", views.excluir, name="agenda_excluir"),
    
    path('api/cliente/<int:cliente_id>/valor/', views.obter_valor_cliente, name='api_valor_cliente'),

    path('excluir-massa/', views.excluir_massa, name='agenda_excluir_massa'),

]