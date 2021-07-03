from logging import getLogger
from importlib import import_module
from django.apps import AppConfig
from django.conf import settings
from django.utils.module_loading import import_string

logger = getLogger(__name__)


class BillingConfig(AppConfig):
    name = "billing"

    def ready(self):
        service_class = import_string(settings.BILLING_SERVICE)
        self.service = service_class()
        logger.info("Using billing service: %s", self.service)
