from django import forms
from .models import Cliente


class ClienteForm(forms.ModelForm):
    nascimento = forms.DateField(
        label="Data de Nascimento",
        required=False,
        input_formats=['%Y-%m-%d', '%d/%m/%Y'],
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = Cliente
        fields = "__all__"  # Inclui todos os campos do modelo de cliente

        widgets = {
            "observacoes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Injeta automaticamente as classes do Bootstrap e placeholders
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.widgets.Select):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'

        # Customizações pontuais de placeholder (opcional)
        if 'dia_vencimento' in self.fields:
            self.fields['dia_vencimento'].widget.attrs['placeholder'] = 'Ex: 5, 10, 15'
        elif 'dias_vencimento' in self.fields:
            self.fields['dias_vencimento'].widget.attrs['placeholder'] = 'Ex: 5, 10, 15'