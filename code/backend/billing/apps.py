from logging import getLogger
from importlib import import_module
from django.apps import AppConfig
from django.conf import settings

logger = getLogger(__name__)


class BillingConfig(AppConfig):
    name = "billing"

    def ready(self):
        self.service = import_module(settings.BILLING_SERVICE)
        logger.info("Using billing service: %s", self.service)
