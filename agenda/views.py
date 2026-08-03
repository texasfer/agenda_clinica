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
    agendamento = get_object_or_404(Agendamento, pk=pk)

    if request.method == 'POST':
        form = AgendamentoForm(request.POST, instance=agendamento)
        
        datas = request.POST.getlist('datas[]')
        horas_inicio = request.POST.getlist('horas_inicio[]')
        horas_fim = request.POST.getlist('horas_fim[]')
        duracao_minutos = request.POST.get('duracao_minutos')

        if form.is_valid():
            obj = form.save(commit=False)

            # Preenche a data e horários
            if datas and datas[0]:
                obj.data = datas[0]
            if horas_inicio and horas_inicio[0]:
                obj.hora_inicio = horas_inicio[0]
            if horas_fim and horas_fim[0] and hasattr(obj, 'hora_fim'):
                obj.hora_fim = horas_fim[0]
            if duracao_minutos and hasattr(obj, 'duracao_minutos'):
                obj.duracao_minutos = int(duracao_minutos)

            # Se o valor não foi informado na tela, busca do cadastro do cliente
            if not obj.valor and obj.cliente:
                obj.valor = obj.cliente.valor_sessao

            obj.save()
            return redirect("agenda")
    else:
        form = AgendamentoForm(instance=agendamento)

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

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from clientes.models import Cliente

@login_required
def obter_valor_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    return JsonResponse({
        'sucesso': True, 
        'valor': float(cliente.valor_sessao)
    })

from financeiro.models import Lancamento  # Importa o model do financeiro

@login_required
def criar_ou_editar_agendamento(request, pk=None):
    if pk:
        agendamento = get_object_or_404(Agendamento, pk=pk)
    else:
        agendamento = Agendamento()

    if request.method == 'POST':
        form = AgendamentoForm(request.POST, instance=agendamento)
        
        datas = request.POST.getlist('datas[]')
        horas_inicio = request.POST.getlist('horas_inicio[]')
        horas_fim = request.POST.getlist('horas_fim[]')
        duracao_minutos = request.POST.get('duracao_minutos')

        if form.is_valid():
            # Salva o agendamento individual ou primeiro da lista
            obj = form.save(commit=False)

            if datas and datas[0]:
                obj.data = datas[0]
            if horas_inicio and horas_inicio[0]:
                obj.hora_inicio = horas_inicio[0]
            if horas_fim and horas_fim[0] and hasattr(obj, 'hora_fim'):
                obj.hora_fim = horas_fim[0]
            if duracao_minutos and hasattr(obj, 'duracao_minutos'):
                obj.duracao_minutos = int(duracao_minutos)

            # Define o valor puxando do cliente se estiver zerado
            if not obj.valor and obj.cliente:
                obj.valor = obj.cliente.valor_sessao

            obj.save()

            # --- GERADOR DE CONTAS A RECEBER (LANÇAMENTO) ---
            if obj.cliente and obj.valor > 0:
                # Calcula a data de vencimento com base no cadastro do cliente
                dias = getattr(obj.cliente, 'dias_vencimento', 5)
                
                if isinstance(obj.data, str):
                    data_agendamento = datetime.strptime(obj.data, '%Y-%m-%d').date()
                else:
                    data_agendamento = obj.data

                data_vencimento = data_agendamento + timedelta(days=dias)

                # Cria ou atualiza o lançamento vinculado a este agendamento
                Lancamento.objects.update_or_create(
                    agendamento=obj,
                    defaults={
                        'cliente': obj.cliente,
                        'descricao': f"Sessão de Consulta - {obj.cliente.nome} ({data_agendamento.strftime('%d/%m/%Y')})",
                        'valor': obj.valor,
                        'data': data_agendamento,
                        'data_vencimento': data_vencimento,
                        'status': 'PENDENTE',
                        'tipo': 'RECEITA'
                    }
                )

            return redirect("agenda")
    else:
        form = AgendamentoForm(instance=agendamento)

    return render(request, "agenda/form.html", {"form": form, "agendamento": agendamento})

from django.shortcuts import redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Agendamento

@require_POST
def excluir_massa(request):
    # Pega todos os IDs marcados nos checkboxes (lista de strings)
    ids = request.POST.getlist("ids")
    
    if ids:
        # Deleta todos os agendamentos cujos IDs estão na lista
        qtd_deletados, _ = Agendamento.objects.filter(id__in=ids).delete()
        messages.success(request, f"{qtd_deletados} agendamento(s) excluído(s) com sucesso!")
    else:
        messages.warning(request, "Nenhum agendamento foi selecionado para exclusão.")

    return redirect("agenda")