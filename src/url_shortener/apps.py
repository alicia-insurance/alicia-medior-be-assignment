from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "url_shortener"

    def ready(self):
        # Import signals to ensure they are registered
        import url_shortener.signals
