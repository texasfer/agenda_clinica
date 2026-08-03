from django.contrib import messages
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
    pesquisa = request.GET.get("q", "")

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
def criar_atendimento(request, agendamento_id=None):
    agendamento = None
    atendimento = None

    if agendamento_id:
        agendamento = get_object_or_404(Agendamento, id=agendamento_id)
        # Recupera ou cria uma instância inicial para vincular ao Form
        atendimento, _ = Atendimento.objects.get_or_create(agendamento=agendamento)

    form = AtendimentoForm(request.POST or None, instance=atendimento)

    if request.method == "POST":
        if form.is_valid():
            atendimento = form.save(commit=False)
            atendimento.finalizado = True
            
            if agendamento:
                atendimento.agendamento = agendamento

            atendimento.save()

            # 1. Atualiza Status na Agenda
            if agendamento:
                agendamento.status = "ATENDIDO"
                agendamento.save()

                # 2. Atualiza Sessões do Cliente
                if agendamento.cliente:
                    cliente = agendamento.cliente
                    cliente.sessoes_realizadas = (cliente.sessoes_realizadas or 0) + 1
                    cliente.save()

                # 3. Lançamento Financeiro
                Lancamento.objects.get_or_create(
                    atendimento=atendimento,
                    defaults={
                        "agendamento": agendamento,
                        "cliente": agendamento.cliente,
                        "data": timezone.now().date(),
                        "valor": agendamento.valor,
                        "status": "PENDENTE"
                    }
                )

            messages.success(request, "Atendimento concluído com sucesso!")
            return redirect("agenda")

    context = {
        "form": form,               # Garante que o {{ form.queixa }}, etc. renderizem
        "agendamento": agendamento, # Garante os dados do topo do HTML
        "agenda": agendamento       # Compatibilidade extra com o template
    }
    return render(request, "atendimento/form.html", context)


@login_required
def editar(request, pk):
    atendimento = get_object_or_404(Atendimento, pk=pk)

    form = AtendimentoForm(
        request.POST or None,
        instance=atendimento
    )

    if form.is_valid():
        form.save()
        messages.success(request, "Atendimento atualizado!")
        return redirect("atendimento")

    return render(
        request,
        "atendimento/form.html",
        {
            "form": form,
            "agendamento": atendimento.agendamento,
            "agenda": atendimento.agendamento
        }
    )


@login_required
def excluir(request, pk):
    atendimento = get_object_or_404(Atendimento, pk=pk)
    atendimento.delete()
    messages.success(request, "Atendimento excluído!")
    return redirect("atendimento")


@login_required
def atendimento_imprimir(request, pk):
    atendimento = get_object_or_404(Atendimento, pk=pk)
    return render(request, 'atendimento/imprimir.html', {'atendimento': atendimento})