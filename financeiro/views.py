from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Lancamento
from .forms import LancamentoForm

# 1. READ / LISTA
@login_required
def lista(request):
    pesquisa = request.GET.get("q", "")
    status_filter = request.GET.get("status", "")

    lancamentos = Lancamento.objects.select_related("cliente", "agendamento").order_by("-data_vencimento")

    if pesquisa:
        lancamentos = lancamentos.filter(cliente__nome__icontains=pesquisa)
    if status_filter:
        lancamentos = lancamentos.filter(status=status_filter)

    return render(request, "financeiro/lista.html", {
        "financeiro": lancamentos,
        "pesquisa": pesquisa,
        "status": status_filter,
    })

# 2. CREATE & UPDATE
@login_required
def salvar_lancamento(request, pk=None):
    if pk:
        lancamento = get_object_or_404(Lancamento, pk=pk)
    else:
        lancamento = Lancamento()

    if request.method == 'POST':
        form = LancamentoForm(request.POST, instance=lancamento)
        if form.is_valid():
            form.save()
            return redirect('financeiro')
    else:
        form = LancamentoForm(instance=lancamento)

    return render(request, 'financeiro/form.html', {'form': form, 'lancamento': lancamento})

# 3. BAixar (Mudar para PAGO)
@login_required
def baixar(request, pk):
    lanc = get_object_or_404(Lancamento, pk=pk)
    lanc.status = "PAGO"
    lanc.save()
    return redirect("financeiro")

# 4. ESTORNAR (Voltar para PENDENTE)
@login_required
def estornar(request, pk):
    lanc = get_object_or_404(Lancamento, pk=pk)
    lanc.status = "PENDENTE"
    lanc.save()
    return redirect("financeiro")

# 5. DELETE
@login_required
def excluir(request, pk):
    lanc = get_object_or_404(Lancamento, pk=pk)
    lanc.delete()
    return redirect("financeiro")

    from django.db.models import Sum, Q
from django.shortcuts import render
from django.utils import timezone
from .models import Lancamento
from agenda.models import Agendamento


def dashboard_financeiro(request):
    hoje = timezone.now()
    mes_atual = hoje.month
    ano_atual = hoje.year

    lancamentos = Lancamento.objects.select_related('cliente', 'agendamento', 'atendimento').order_by('-data_vencimento')

    # --- TOTAIS GERAIS (ACUMULADO) ---
    total_previsto = lancamentos.filter(
        Q(status="PREVISTO") | Q(status="AGENDADO")
    ).aggregate(Sum('valor'))['valor__sum'] or 0

    total_a_receber = lancamentos.filter(
        Q(status="A_RECEBER") | Q(status="ATENDIDO")
    ).aggregate(Sum('valor'))['valor__sum'] or 0

    total_pago = lancamentos.filter(status="PAGO").aggregate(Sum('valor'))['valor__sum'] or 0

    # Fallback caso os lançamentos ainda não existam no banco
    if total_previsto == 0:
        total_previsto = Agendamento.objects.filter(
            status__in=["AGENDADO", "CONFIRMADO"]
        ).aggregate(Sum('valor'))['valor__sum'] or 0

    if total_a_receber == 0:
        total_a_receber = Agendamento.objects.filter(
            status="ATENDIDO"
        ).aggregate(Sum('valor'))['valor__sum'] or 0

    # --- TOTAIS DO MÊS ATUAL ---
    # Considera a data de vencimento ou a data do agendamento caindo no mês/ano atual
    a_receber_mes = lancamentos.filter(
        Q(status="A_RECEBER") | Q(status="ATENDIDO"),
        data_vencimento__month=mes_atual,
        data_vencimento__year=ano_atual
    ).aggregate(Sum('valor'))['valor__sum'] or 0

    agendado_mes = lancamentos.filter(
        Q(status="PREVISTO") | Q(status="AGENDADO"),
        data_vencimento__month=mes_atual,
        data_vencimento__year=ano_atual
    ).aggregate(Sum('valor'))['valor__sum'] or 0

    # Fallback do mês direto na agenda se necessário
    if agendado_mes == 0:
        agendado_mes = Agendamento.objects.filter(
            status__in=["AGENDADO", "CONFIRMADO"],
            data__month=mes_atual,
            data__year=ano_atual
        ).aggregate(Sum('valor'))['valor__sum'] or 0

    if a_receber_mes == 0:
        a_receber_mes = Agendamento.objects.filter(
            status="ATENDIDO",
            data__month=mes_atual,
            data__year=ano_atual
        ).aggregate(Sum('valor'))['valor__sum'] or 0

    context = {
        "lancamentos": lancamentos,
        # Totais Gerais
        "total_previsto": total_previsto,
        "total_a_receber": total_a_receber,
        "total_pago": total_pago,
        # Totais do Mês
        "a_receber_mes": a_receber_mes,
        "agendado_mes": agendado_mes,
        "mes_nome": hoje.strftime('%B').title(), # Nome do mês para o cabeçalho
    }
    return render(request, "financeiro/dashboard.html", context)