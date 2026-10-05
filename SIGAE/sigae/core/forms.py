from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.utils import timezone

from .models import Reserva, Turno


class _Bootstrap:
    def _style(self):
        for f in self.fields.values():
            f.widget.attrs["class"] = "form-select" if isinstance(f.widget, forms.Select) else "form-control"


class ReservaForm(_Bootstrap, forms.Form):
    data = forms.DateField(label="Data", widget=forms.DateInput(attrs={"type": "date"}))
    turno = forms.ChoiceField(label="Turno", choices=Turno.choices)
    quantidade = forms.IntegerField(label="Quantidade de notebooks", min_value=1, max_value=45, initial=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["data"].initial = timezone.localdate()
        self._style()

    def clean_data(self):
        d = self.cleaned_data["data"]
        if d < timezone.localdate():
            raise forms.ValidationError("A data não pode estar no passado.")
        return d


class SenhaForm(_Bootstrap, PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style()


class ReservaFiltroForm(_Bootstrap, forms.Form):
    data = forms.DateField(label="Data", required=False, widget=forms.DateInput(attrs={"type": "date"}))
    turno = forms.ChoiceField(label="Turno", required=False, choices=[("", "Todos")] + list(Turno.choices))
    equipamento = forms.IntegerField(label="Nº do equipamento", required=False, min_value=1, max_value=45)
    status = forms.ChoiceField(label="Status", required=False, choices=[("", "Todos")] + list(Reserva.Status.choices))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["equipamento"].widget.attrs["placeholder"] = "1 a 45"
        self._style()


class EmprestimoFiltroForm(ReservaFiltroForm):
    codigo = forms.IntegerField(label="Cód. de Empréstimo", required=False, min_value=1)
    field_order = ["codigo", "data", "turno", "equipamento", "status"]
