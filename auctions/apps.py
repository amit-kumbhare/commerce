"""Django app configuration.

Defines app metadata and initialization. The AppConfig subclass allows custom
app behavior like ready() signal handling. Referenced in settings.INSTALLED_APPS
for Django to recognize this as an installed application.
"""
from django.apps import AppConfig


class AuctionsConfig(AppConfig):
    name = 'auctions'
