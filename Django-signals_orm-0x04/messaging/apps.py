# messaging_app/apps.py
from django.apps import AppConfig

class MessagingAppConfig(AppConfig):
    name = 'messaging_app'

    def ready(self):
        import messaging_app.signals  # 👈 Ensures signal is registered

