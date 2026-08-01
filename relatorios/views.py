from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from clientes.models import Cliente
from agenda.models import Agendamento
from atendimento.models import Atendimento
from financeiro.models import Lancamento


@login_required
def index(request):

    return render(
        request,
        "relatorios/index.html"
    )


@login_required
def clientes(request):

    return render(

        request,

        "relatorios/clientes.html",

        {

            "clientes":

            Cliente.objects.order_by("nome")

        }

    )


@login_required
def agenda(request):

    return render(

        request,

        "relatorios/agenda.html",

        {

            "agenda":

            Agendamento.objects.select_related(

                "cliente",

                "profissional"

            )

        }

    )


@login_required
def atendimentos(request):

    return render(

        request,

        "relatorios/atendimentos.html",

        {

            "atendimentos":

            Atendimento.objects.select_related(

                "agendamento",

                "agendamento__cliente"

            )

        }

    )


@login_required
def financeiro(request):

    return render(

        request,

        "relatorios/financeiro.html",

        {

            "financeiro":

            Lancamento.objects.select_related(

                "cliente"

            )

        }

    )