from django.apps import AppConfig


class ConfessionConfig(AppConfig):
    name = 'confession'

    def ready(self):
        import confession.tasks
