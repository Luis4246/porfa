from django.db import connection
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.apps import apps

def _is_mysql():
    return connection.vendor == "mysql"

def _reset_autoincrement(model):
    if not _is_mysql():
        return
    table = connection.ops.quote_name(model._meta.db_table)
    with connection.cursor() as cursor:
        cursor.execute(f"ALTER TABLE {table} AUTO_INCREMENT = 1")

@receiver(post_delete)
def reset_ai_reserva_si_vacia(sender, **kwargs):
    if sender.__name__ == "Reserva":
        Reserva = apps.get_model('itemApp', 'Reserva')
        if not Reserva.objects.exists():
            _reset_autoincrement(Reserva)

@receiver(post_delete)
def reset_ai_mesa_si_vacia(sender, **kwargs):
    if sender.__name__ == "Mesa":
        Mesa = apps.get_model('itemApp', 'Mesa')
        if not Mesa.objects.exists():
            _reset_autoincrement(Mesa)
