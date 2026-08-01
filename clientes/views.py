from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages

from .models import Cliente
from .forms import ClienteForm


@login_required
def lista(request):

    pesquisa = request.GET.get("q", "")

    clientes = Cliente.objects.all()

    if pesquisa:
        clientes = clientes.filter(
            Q(nome__icontains=pesquisa) |
            Q(cpf__icontains=pesquisa) |
            Q(telefone__icontains=pesquisa) |
            Q(whatsapp__icontains=pesquisa)
        )

    return render(
        request,
        "clientes/lista.html",
        {
            "clientes": clientes,
            "pesquisa": pesquisa
        }
    )


@login_required
def novo(request):

    form = ClienteForm(request.POST or None)

    if form.is_valid():

        form.save()

        messages.success(
            request,
            "Cliente salvo com sucesso!"
        )

        return redirect("clientes")
    return render(
        request,
        "clientes/form.html",
        {"form": form}
    )


@login_required
def editar(request, pk):

    cliente = get_object_or_404(
        Cliente,
        pk=pk
    )

    form = ClienteForm(
        request.POST or None,
        instance=cliente
    )
    
    if form.is_valid():

        form.save()

        messages.success(
            request,
            "Editado salvo com sucesso!"
        )

        return redirect("clientes")

    return render(
        request,
        "clientes/form.html",
        {
            "form": form,
            "cliente": cliente
        }
    )


@login_required
def excluir(request, pk):

    cliente = get_object_or_404(
        Cliente,
        pk=pk
    )

    cliente.delete()

    return redirect("clientes")