from django.apps import AppConfig


class ResturantConfig(AppConfig):
    name = 'resturant'

    def ready(self):
        import resturant.signals
