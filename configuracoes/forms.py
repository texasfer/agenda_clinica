from django import forms
from .models import Configuracao


class ConfiguracaoForm(forms.ModelForm):

    class Meta:

        model = Configuracao

        fields = "__all__"

        widgets = {

            "inicio_expediente": forms.TimeInput(
                attrs={
                    "type":"time"
                }
            ),

            "fim_expediente": forms.TimeInput(
                attrs={
                    "type":"time"
                }
            ),

        }

    def __init__(self,*args,**kwargs):

        super().__init__(*args,**kwargs)

        for campo in self.fields.values():

            campo.widget.attrs.setdefault(
                "class",
                "form-control"
            )