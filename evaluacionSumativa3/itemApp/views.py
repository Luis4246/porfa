from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Reserva
from .forms import ReservaForm

def reserva_list(request):
    reservas = Reserva.objects.all().order_by("-fecha", "-hora")
    return render(request, "itemApp/reserva_list.html", {"reservas": reservas})

def reserva_create(request):
    if request.method == "POST":
        form = ReservaForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Reserva creada correctamente.")
                return redirect("reserva_list")
            except (IntegrityError, ValidationError):
                messages.error(request, "Esta mesa ya está reservada en esa fecha y hora o los datos no son válidos.")
        else:
            messages.error(request, "Corrige los errores del formulario.")
    else:
        form = ReservaForm()
    return render(request, "itemApp/reserva_form.html", {"form": form, "titulo": "Nueva Reserva"})

def reserva_update(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    if request.method == "POST":
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Reserva actualizada correctamente.")
                return redirect("reserva_list")
            except (IntegrityError, ValidationError):
                messages.error(request, "Esta mesa ya está reservada en esa fecha y hora o los datos no son válidos.")
        else:
            messages.error(request, "Corrige los errores del formulario.")
    else:
        form = ReservaForm(instance=reserva)
    return render(request, "itemApp/reserva_form.html", {"form": form, "titulo": "Editar Reserva"})

def reserva_delete(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    if request.method == "POST":
        reserva.delete()
        messages.success(request, "Reserva eliminada correctamente.")
        return redirect("reserva_list")
    return render(request, "itemApp/reserva_confirm_delete.html", {"reserva": reserva})
