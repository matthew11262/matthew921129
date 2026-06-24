from django.apps import AppConfig


class MainappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mainapp'

    def ready(self):
        from .mqtt_service import mqtt_handler
        mqtt_handler.start_mqtt_client()
