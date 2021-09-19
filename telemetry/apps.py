from importlib import import_module
from django.db.models.signals import post_migrate

from django.apps import AppConfig

class TelemetryConfig(AppConfig):
    name = 'telemetry'

        
