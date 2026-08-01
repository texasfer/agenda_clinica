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



@login_required
def dashboard(request):
    hoje = date.today()

    # Captura os filtros da requisição (se não passados, assume o mês e ano atuais)
    mes_selecionado = int(request.GET.get('mes', hoje.month))
    ano_selecionado = int(request.GET.get('ano', hoje.year))

    # Lista de anos para o select (do ano atual 2 anos para trás e 1 para frente)
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

    # Métricas do Período Selecionado
    agendamentos_mes = agendamentos_filtrados.count()
    atendimentos_mes = agendamentos_filtrados.filter(status__iexact='ATENDIDO').count()

    resultado_faturamento = agendamentos_filtrados.aggregate(total=Sum('valor'))
    faturamento_mes = resultado_faturamento['total'] or 0.00

    # Total de agendamentos no Ano Inteiro Selecionado
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