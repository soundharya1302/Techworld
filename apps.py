from django.apps import AppConfig


class TicketappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ticketapp'

def ready(self):
        # Avoid database operations here
        pass