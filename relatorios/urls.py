from django.urls import path

from . import views

urlpatterns=[

path("",views.index,name="relatorios"),

path("clientes/",views.clientes,name="relatorio_clientes"),

path("agenda/",views.agenda,name="relatorio_agenda"),

path("atendimentos/",views.atendimentos,name="relatorio_atendimentos"),

path("financeiro/",views.financeiro,name="relatorio_financeiro"),

]