from django.apps import AppConfig


class OkrConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'OKR'

    def ready(self):    
        import OKR.signals