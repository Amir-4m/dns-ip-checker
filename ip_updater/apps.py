from django.apps import AppConfig


class IpUpdaterConfig(AppConfig):
    name = 'ip_updater'

    def ready(self):
        import ip_updater.signals
