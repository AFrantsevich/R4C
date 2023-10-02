from django.apps import AppConfig


class RobotsConfig(AppConfig):
    name = 'robots'

    def ready(self):
        from orders.callbacks import callback_order
