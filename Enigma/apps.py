from django.apps import AppConfig

class EnigmaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Enigma'

    def ready(self):
        import Enigma.signals   