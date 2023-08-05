from django.apps import AppConfig


class AppConfigurationsConfig(AppConfig):
    name = 'app_configurations'

    def ready(self):
        import app_configurations.signals
