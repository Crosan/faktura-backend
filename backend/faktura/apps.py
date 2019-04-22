from django.apps import AppConfig


class FakturaConfig(AppConfig):
    name = 'backend.faktura'

    def ready(self):
        import backend.faktura.signals.handlers