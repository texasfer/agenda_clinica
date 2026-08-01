from django import forms
from .models import Cliente


class ClienteForm(forms.ModelForm):
    # Sobrescrevemos apenas a data para aceitar o formato vindo do HTML
    nascimento = forms.DateField(
        label="Data de Nascimento",
        required=False, # Mude para True se for um campo obrigatório
        input_formats=['%Y-%m-%d', '%d/%m/%Y'], # Aceita o formato HTML5 (AAAA-MM-DD) e o padrão BR (DD/MM/AAAA)
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date', # Garante que o input no navegador seja o seletor de data
                'class': 'form-control', # Mantenha a classe CSS que você usa (ex: Bootstrap)
            }
        )
    )

    class Meta:

        model=Cliente

        fields="__all__"

        exclude = [
                        "sessoes_realizadas",
                    ]

        widgets={

            "nascimento":forms.DateInput(

                attrs={"type":"date"}

            ),

            "observacoes":forms.Textarea(

                attrs={"rows":4}

            ),


        }