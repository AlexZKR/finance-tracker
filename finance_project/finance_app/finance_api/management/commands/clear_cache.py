import logging
from django.core.management.base import BaseCommand
from django.core.cache import cache

logger = logging.getLogger("__name__")


class Command(BaseCommand):
    def handle(self, *args, **options):
        logger.info("Cache clearing command execution...")
        cache.clear()
        self.stdout.write("Cache cleared \n")
