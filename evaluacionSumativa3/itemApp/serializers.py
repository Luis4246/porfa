from rest_framework import serializers
from .models import Reserva, Mesa

class MesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mesa
        fields = "__all__"

class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = "__all__"

    def validate(self, attrs):
        mesa = attrs.get("mesa") or getattr(self.instance, "mesa", None)
        fecha = attrs.get("fecha") or getattr(self.instance, "fecha", None)
        hora = attrs.get("hora") or getattr(self.instance, "hora", None)
        personas = attrs.get("personas") or getattr(self.instance, "personas", None)

        if mesa and personas and personas > mesa.capacidad:
            raise serializers.ValidationError({"mesa": f"La mesa {mesa.numero} solo admite {mesa.capacidad} personas."})

        if mesa and fecha and hora:
            qs = Reserva.objects.filter(mesa=mesa, fecha=fecha, hora=hora)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError({"mesa": "Esta mesa ya está reservada en esa fecha y hora."})
        return attrs
