from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Crea superusuario admin/secret si no existe"

    def handle(self, *args, **kwargs):
        User = get_user_model()
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin","admin@example.com","secret")
            self.stdout.write(self.style.SUCCESS("Creado admin/secret"))
        else:
            self.stdout.write(self.style.WARNING("admin ya existe"))
