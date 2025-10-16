from django.db import models
from django.core.exceptions import ValidationError

class Mesa(models.Model):
    numero = models.IntegerField(unique=True)
    capacidad = models.PositiveIntegerField()

    def __str__(self):
        return f"Mesa {self.numero} (cap. {self.capacidad})"

class Reserva(models.Model):
    ESTADOS = [
        ("RESERVADO", "RESERVADO"),
        ("COMPLETADA", "COMPLETADA"),
        ("ANULADA", "ANULADA"),
        ("NO_ASISTEN", "NO_ASISTEN"),
    ]

    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    fecha = models.DateField()
    hora = models.TimeField()
    personas = models.PositiveIntegerField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default="RESERVADO")
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    observacion = models.TextField(blank=True, null=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["mesa", "fecha", "hora"], name="uniq_reserva_mesa_fecha_hora")
        ]

    def __str__(self):
        return f"{self.nombre} ({self.fecha} {self.hora})"

    def clean(self):
        super().clean()
        if self.mesa_id and self.personas is not None:
            m = Mesa.objects.filter(pk=self.mesa_id).values("capacidad", "numero").first()
            if m and self.personas > m["capacidad"]:
                raise ValidationError({"mesa": f"La mesa {m['numero']} solo admite {m['capacidad']} personas."})
        if self.mesa_id and self.fecha and self.hora:
            existe = (Reserva.objects
                      .filter(mesa_id=self.mesa_id, fecha=self.fecha, hora=self.hora)
                      .exclude(pk=self.pk).exists())
            if existe:
                raise ValidationError({"mesa": "Esta mesa ya está reservada en esa fecha y hora."})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
