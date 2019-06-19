from django.apps import AppConfig


class IpUpdaterConfig(AppConfig):
    name = 'dns_updater'

    def ready(self):
        import dns_updater.signals
