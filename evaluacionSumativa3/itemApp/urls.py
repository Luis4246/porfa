from django.urls import path
from . import views
from .api import ReservaListCreate, ReservaDetail

urlpatterns = [
    path("", views.reserva_list, name="reserva_list"),
    path("nueva/", views.reserva_create, name="reserva_create"),
    path("<int:pk>/editar/", views.reserva_update, name="reserva_update"),
    path("<int:pk>/eliminar/", views.reserva_delete, name="reserva_delete"),
    path("api/reservas/", ReservaListCreate.as_view(), name="api_reserva_list_create"),
    path("api/reservas/<int:pk>/", ReservaDetail.as_view(), name="api_reserva_detail"),
]
