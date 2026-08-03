from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum, Count
from datetime import date
import calendar
from django.db.models.functions import TruncDay, TruncMonth  # <--- Adicionado TruncDay aqui
# Ajuste os imports para apontar para os seus modelos
from clientes.models import Cliente
from agenda.models import Agendamento


def login_view(request):

    if request.method=="POST":

        usuario=request.POST.get("usuario")

        senha=request.POST.get("senha")

        user=authenticate(
            request,
            username=usuario,
            password=senha
        )

        if user:

            login(request,user)

            return redirect("dashboard")

        return render(request,"usuarios/login.html",{
        "erro":"Usuário ou senha inválidos."
    })
    return render(request,"usuarios/login.html")


from datetime import date
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.db.models.functions import TruncDay
from django.shortcuts import render, redirect

from agenda.models import Agendamento
from clientes.models import Cliente

from datetime import date
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Q
from django.db.models.functions import TruncDay
from django.shortcuts import render, redirect

from agenda.models import Agendamento
from clientes.models import Cliente


@login_required
def dashboard(request):
    hoje = date.today()

    # Captura os filtros da requisição (se não passados, assume mês e ano atuais)
    mes_selecionado = int(request.GET.get('mes', hoje.month))
    ano_selecionado = int(request.GET.get('ano', hoje.year))

    # Lista de anos e meses para o select
    anos_disponiveis = range(hoje.year - 2, hoje.year + 2)
    meses_disponiveis = [
        (1, 'Janeiro'), (2, 'Fevereiro'), (3, 'Março'), (4, 'Abril'),
        (5, 'Maio'), (6, 'Junho'), (7, 'Julho'), (8, 'Agosto'),
        (9, 'Setembro'), (10, 'Outubro'), (11, 'Novembro'), (12, 'Dezembro')
    ]

    # Totais Gerais do Sistema
    total_clientes = Cliente.objects.count()
    total_agendados = Agendamento.objects.count()
    total_atendidos = Agendamento.objects.filter(status__iexact='ATENDIDO').count()

    # Base filtrada conforme Mês e Ano selecionados
    agendamentos_filtrados = Agendamento.objects.filter(
        data__year=ano_selecionado,
        data__month=mes_selecionado
    )

    # ==========================================
    # CÁLCULOS DA VISÃO FINANCEIRA
    # ==========================================

    # 1. VALORES DO MÊS SELECIONADO
    previsto_mes = agendamentos_filtrados.filter(
        status__iexact='AGENDADO'
    ).aggregate(total=Sum('valor'))['total'] or 0.00

    a_receber_mes = agendamentos_filtrados.filter(
        status__iexact='ATENDIDO'
    ).aggregate(total=Sum('valor'))['total'] or 0.00

    faturamento_mes = previsto_mes + a_receber_mes

    # 2. VALORES TOTAIS (GERAL ACUMULADO NO SISTEMA)
    total_previsto_geral = Agendamento.objects.filter(
        status__iexact='AGENDADO'
    ).aggregate(total=Sum('valor'))['total'] or 0.00

    total_a_receber_geral = Agendamento.objects.filter(
        status__iexact='ATENDIDO'
    ).aggregate(total=Sum('valor'))['total'] or 0.00

    total_geral_acumulado = total_previsto_geral + total_a_receber_geral

    # Métricas adicionais do período
    agendamentos_mes = agendamentos_filtrados.count()
    atendimentos_mes = agendamentos_filtrados.filter(status__iexact='ATENDIDO').count()
    agendamentos_ano = Agendamento.objects.filter(data__year=ano_selecionado).count()

    # --- DADOS PARA O GRÁFICO (Agrupado por Dia dentro do Mês selecionado) ---
    agendamentos_por_dia = (
        agendamentos_filtrados
        .annotate(dia=TruncDay('data'))
        .values('dia')
        .annotate(total=Count('id'))
        .order_by('dia')
    )

    grafico_labels = []
    grafico_data = []

    for item in agendamentos_por_dia:
        if item['dia']:
            grafico_labels.append(item['dia'].strftime('%d/%m'))
            grafico_data.append(item['total'])

    # Próximos 10 agendamentos gerais a partir de hoje
    proximos = Agendamento.objects.filter(data__gte=hoje).order_by('data', 'hora_inicio')[:10]

    context = {
        # Métricas Globais
        'clientes': total_clientes,
        'agendados': total_agendados,
        'atendidos': total_atendidos,

        # Métricas do Filtro Selecionado
        'agendamentos_mes': agendamentos_mes,
        'atendimentos_mes': atendimentos_mes,
        'agendamentos_ano': agendamentos_ano,
        'faturamento_mes': faturamento_mes,

        # --- VISÃO FINANCEIRA ---
        # Do Mês Selecionado
        'previsto_mes': previsto_mes,
        'a_receber_mes': a_receber_mes,
        
        # Totais Acumulados Gerais
        'total_previsto_geral': total_previsto_geral,
        'total_a_receber_geral': total_a_receber_geral,
        'total_geral_acumulado': total_geral_acumulado,

        # Dados do Filtro
        'mes_selecionado': mes_selecionado,
        'ano_selecionado': ano_selecionado,
        'meses_disponiveis': meses_disponiveis,
        'anos_disponiveis': anos_disponiveis,

        # Gráfico e Próximos
        'grafico_labels': grafico_labels,
        'grafico_data': grafico_data,
        'proximos': proximos,
    }

    return render(request, "usuarios/dashboard.html", context)


def logout_view(request):
    logout(request)
    return redirect("login")

def logout_view(request):
    logout(request)
    return redirect("login")