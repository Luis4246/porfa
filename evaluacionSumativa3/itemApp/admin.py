from django.contrib import admin
from .models import Reserva, Mesa

@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = ("numero", "capacidad")
    search_fields = ("numero",)

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = (
        "nombre", "telefono", "fecha", "hora",
        "personas",      
        "estado", "mesa", "creado",
    )
    list_filter = ("estado", "fecha", "mesa")
    search_fields = ("nombre", "telefono")
