from django import forms
from .models import Atendimento


class AtendimentoForm(forms.ModelForm):

    class Meta:

        model = Atendimento

        exclude = (
            "agendamento",
            "finalizado",
        )

        widgets = {

            "queixa": forms.Textarea(attrs={"rows":3}),

            "anamnese": forms.Textarea(attrs={"rows":4}),

            "evolucao": forms.Textarea(attrs={"rows":4}),

            "procedimentos": forms.Textarea(attrs={"rows":3}),

            "conduta": forms.Textarea(attrs={"rows":3}),

            "observacoes": forms.Textarea(attrs={"rows":3}),

        }

    def __init__(self,*args,**kwargs):

        super().__init__(*args,**kwargs)

        for campo in self.fields.values():

            campo.widget.attrs["class"]="form-control"