from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect

from .models import Configuracao
from .forms import ConfiguracaoForm


@login_required
def empresa(request):

    config = Configuracao.objects.first()

    if not config:

        config = Configuracao.objects.create(
            nome_empresa="Minha Clínica"
        )

    form = ConfiguracaoForm(

        request.POST or None,

        request.FILES or None,

        instance=config

    )

    if form.is_valid():

        form.save()

        return redirect("config_empresa")

    return render(

        request,

        "configuracoes/empresa.html",

        {

            "form":form

        }

    )