from django.apps import AppConfig


class ProxybotConfig(AppConfig):
    name = 'promoter'

    def ready(self):
        import promoter.signals
