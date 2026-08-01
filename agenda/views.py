from django.contrib import messages  # <--- CERTIFIQUE-SE DE QUE ESTÁ ASSIM

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from datetime import datetime
from .models import Agendamento
from .forms import AgendamentoForm


@login_required
def lista(request):

    pesquisa = request.GET.get("q", "")

    agendamentos = Agendamento.objects.select_related(
        "cliente",
        "profissional"
    )

    if pesquisa:

        agendamentos = agendamentos.filter(
            Q(cliente__nome__icontains=pesquisa)
        )

    return render(
        request,
        "agenda/lista.html",
        {
            "agendamentos": agendamentos,
            "pesquisa": pesquisa,
        },
    )


@login_required
def novo(request):
    if request.method == "POST":
        form = AgendamentoForm(request.POST)

        # Captura as listas de datas e horários enviadas pelo formulário
        datas = request.POST.getlist('datas[]')
        horas_inicio = request.POST.getlist('horas_inicio[]')
        horas_fim = request.POST.getlist('horas_fim[]')

        # Validação do formulário (valida cliente, profissional, valor, etc)
        if form.is_valid():
            cliente = form.cleaned_data['cliente']
            profissional = form.cleaned_data.get('profissional')
            valor = form.cleaned_data.get('valor')
            status = form.cleaned_data.get('status')
            observacoes = form.cleaned_data.get('observacoes')

            total_salvo = 0

            # Percorre cada data/hora gerada no HTML
            for d, hi, hf in zip(datas, horas_inicio, horas_fim):
                if d and hi:  # Se a data e hora inicial estiverem preenchidas
                    
                    # Converte de string para os tipos corretos de Data e Hora se necessário
                    # Se seus campos no Model forem DateField e TimeField:
                    data_obj = datetime.strptime(d, '%Y-%m-%d').date()
                    hora_inicio_obj = datetime.strptime(hi, '%H:%M').time()
                    hora_fim_obj = datetime.strptime(hf, '%H:%M').time() if hf else None

                    # Cria o registro direto no banco
                    Agendamento.objects.create(
                        cliente=cliente,
                        profissional=profissional,
                        valor=valor,
                        status=status,
                        observacoes=observacoes,
                        data=data_obj,
                        hora_inicio=hora_inicio_obj,
                        hora_fim=hora_fim_obj
                    )
                    total_salvo += 1

            messages.success(request, f"{total_salvo} agendamento(s) salvo(s) com sucesso!")
            return redirect("agenda")  # Ou o nome da sua URL de listagem
        else:
            # Imprime os erros no terminal para ajudar no depuramento
            print("Erros do Form:", form.errors)
    else:
        form = AgendamentoForm()

    return render(request, "agenda/form.html", {"form": form})

        


@login_required
def editar(request, pk):

    agendamento = get_object_or_404(
        Agendamento,
        pk=pk,
    )

    form = AgendamentoForm(
        request.POST or None,
        instance=agendamento,
    )

    if form.is_valid():

        form.save()

        return redirect("agenda")

    return render(
        request,
        "agenda/form.html",
        {
            "form": form,
            "agendamento": agendamento,
        },
    )


@login_required
def excluir(request, pk):

    agendamento = get_object_or_404(
        Agendamento,
        pk=pk,
    )

    agendamento.delete()

    return redirect("agenda")