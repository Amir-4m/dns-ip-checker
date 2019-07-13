from django.apps import AppConfig


class ProxybotConfig(AppConfig):
    name = 'proxybot'

    def ready(self):
        import proxybot.signals
