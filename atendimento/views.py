from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from agenda.models import Agendamento
from clientes.models import Cliente
from financeiro.models import Lancamento

from .models import Atendimento
from .forms import AtendimentoForm

@login_required
def lista(request):

    pesquisa = request.GET.get("q","")

    atendimentos = Atendimento.objects.select_related(
        "agendamento",
        "agendamento__cliente",
        "agendamento__profissional"
    )

    if pesquisa:

        atendimentos = atendimentos.filter(
            agendamento__cliente__nome__icontains=pesquisa
        )

    return render(
        request,
        "atendimento/lista.html",
        {
            "atendimentos": atendimentos,
            "pesquisa": pesquisa
        }
    )

@login_required
def novo(request, agendamento_id):

    agenda = get_object_or_404(
        Agendamento,
        pk=agendamento_id
    )

    atendimento, criado = Atendimento.objects.get_or_create(
        agendamento=agenda
    )

    form = AtendimentoForm(
        request.POST or None,
        instance=atendimento
    )

    if form.is_valid():

        atendimento = form.save(commit=False)

        atendimento.finalizado = True

        atendimento.save()

        # Atualiza agenda
        agenda.status = "ATENDIDO"
        agenda.save()

        # Atualiza cliente
        cliente = agenda.cliente

        cliente.sessoes_realizadas += 1

        cliente.save()

        # Financeiro
        Lancamento.objects.get_or_create(

            atendimento=atendimento,

            defaults={

                "cliente": cliente,

                "data": timezone.now().date(),

                "valor": agenda.valor,

                "status": "PENDENTE"

            }

        )

        return redirect("agenda")

    return render(

        request,

        "atendimento/form.html",

        {

            "form": form,

            "agenda": agenda

        }

    )

@login_required
def editar(request, pk):

    atendimento = get_object_or_404(
        Atendimento,
        pk=pk
    )

    form = AtendimentoForm(
        request.POST or None,
        instance=atendimento
    )

    if form.is_valid():

        form.save()

        return redirect("atendimento")

    return render(
        request,
        "atendimento/form.html",
        {
            "form": form,
            "agenda": atendimento.agendamento
        }
    )


@login_required
def excluir(request, pk):

    atendimento = get_object_or_404(
        Atendimento,
        pk=pk
    )

    atendimento.delete()

    return redirect("atendimento")

@login_required
def atendimento_imprimir(request, pk):
    # Busca o atendimento pelo ID (ou lança 404 se não existir)
    atendimento = get_object_or_404(Atendimento, pk=pk)
    
    context = {
        'atendimento': atendimento,
    }
    
    # Renderiza o template formatado para impressão
    return render(request, 'atendimento/imprimir.html', context)

