from django import forms
from .models import Agendamento


class AgendamentoForm(forms.ModelForm):
    # Tornamos não obrigatórios no Form porque são validados na View via request.POST.getlist
    data = forms.DateField(required=False)
    hora_inicio = forms.TimeField(required=False)
    hora_fim = forms.TimeField(required=False)

    class Meta:

        model = Agendamento

        fields = "__all__"

        widgets = {

            "data": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control"
                }
            ),

            "hora_inicio": forms.TimeInput(
                attrs={
                    "type": "time",
                    "class": "form-control"
                }
            ),

            "hora_fim": forms.TimeInput(
                attrs={
                    "type": "time",
                    "class": "form-control"
                }
            ),

            "observacoes": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "form-control"
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for campo in self.fields.values():

            campo.widget.attrs.setdefault(
                "class",
                "form-control"
            )