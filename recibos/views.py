from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required

from financeiro.models import Lancamento


@login_required
def imprimir(request,pk):

    lancamento=get_object_or_404(

        Lancamento,

        pk=pk

    )

    return render(

        request,

        "recibos/imprimir.html",

        {

            "lancamento":lancamento

        }

    )