from django import forms
from .models import Reserva, Mesa

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ["nombre", "telefono", "fecha", "hora", "personas", "estado", "mesa", "observacion"]
        widgets = {
            "fecha": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            "hora": forms.TimeInput(format="%H:%M", attrs={"type": "time"}),
            "observacion": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["fecha"].input_formats = ["%Y-%m-%d"]
        self.fields["hora"].input_formats = ["%H:%M", "%H:%M:%S"]
        self.fields["mesa"].queryset = Mesa.objects.all().order_by("numero")
        self.fields["mesa"].empty_label = "Seleccione una mesa"
        self.fields["personas"].widget.attrs.update({"min": 1, "max": 15})
        estado_field = self.fields["estado"]
        estado_field.required = True
        estado_field.choices = [("", "Seleccione un estado")] + list(Reserva.ESTADOS)
        estado_field.initial = ""

    def clean(self):
        cleaned = super().clean()
        mesa = cleaned.get("mesa")
        personas = cleaned.get("personas")
        fecha = cleaned.get("fecha")
        hora = cleaned.get("hora")

        if mesa and personas and personas > mesa.capacidad:
            self.add_error("mesa", f"La mesa {mesa.numero} solo admite {mesa.capacidad} personas.")

        if mesa and fecha and hora:
            from .models import Reserva as R
            qs = R.objects.filter(mesa=mesa, fecha=fecha, hora=hora)
            if getattr(self.instance, "pk", None):
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                self.add_error("mesa", "Esta mesa ya está reservada en esa fecha y hora.")
        return cleaned
