from django.apps import AppConfig

class ItemAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "itemApp"

    def ready(self):
        import itemApp.signals
