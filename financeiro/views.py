from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Q

from .models import Lancamento


@login_required
def lista(request):

    pesquisa = request.GET.get("q", "")

    status = request.GET.get("status", "")

    financeiro = Lancamento.objects.select_related(
        "cliente",
        "atendimento"
    ).order_by("-data")

    if pesquisa:

        financeiro = financeiro.filter(
            Q(cliente__nome__icontains=pesquisa)
        )

    if status:

        financeiro = financeiro.filter(
            status=status
        )

    total_receber = financeiro.filter(
        status="PENDENTE"
    ).aggregate(
        total=Sum("valor")
    )["total"] or 0

    total_pago = financeiro.filter(
        status="PAGO"
    ).aggregate(
        total=Sum("valor")
    )["total"] or 0

    return render(

        request,

        "financeiro/lista.html",

        {

            "financeiro": financeiro,

            "pesquisa": pesquisa,

            "status": status,

            "total_receber": total_receber,

            "total_pago": total_pago,

        }

    )


@login_required
def baixar(request, pk):

    lanc = get_object_or_404(
        Lancamento,
        pk=pk
    )

    lanc.status = "PAGO"

    lanc.save()

    return redirect("financeiro")


@login_required
def estornar(request, pk):

    lanc = get_object_or_404(
        Lancamento,
        pk=pk
    )

    lanc.status = "PENDENTE"

    lanc.save()

    return redirect("financeiro")


@login_required
def excluir(request, pk):

    get_object_or_404(
        Lancamento,
        pk=pk
    ).delete()

    return redirect("financeiro")