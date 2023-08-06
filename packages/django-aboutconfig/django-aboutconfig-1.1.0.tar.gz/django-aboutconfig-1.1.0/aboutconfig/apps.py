"""Module configuration objects."""

from typing import Any

from django.apps import AppConfig
from django.conf import settings
from django.db import DatabaseError

from . import utils


def _set(key: str, default: Any) -> None:
    key = "ABOUTCONFIG_%s" % key
    setattr(settings, key, getattr(settings, key, default))


class AboutconfigConfig(AppConfig):
    """Configuration provider for the module.

    Ensures configuration is loaded into cache on application start-up."""

    name = "aboutconfig"

    @classmethod
    def ready(cls) -> None:
        _set("CACHE_NAME", "default")
        _set("CACHE_TTL", None)
        _set("AUTOLOAD", True)

        # can't load data if models don't exist in the db yet
        if settings.ABOUTCONFIG_AUTOLOAD and cls.migrations_applied():
            utils.preload_cache()

    @classmethod
    def migrations_applied(cls) -> bool:
        """Check if module's migrations have been applied yet."""

        # pylint: disable=import-outside-toplevel
        from django.db.migrations.loader import MigrationLoader
        from django.db import connection

        try:
            loader = MigrationLoader(connection, ignore_no_migrations=True)
            return (cls.name, "0002_initial_data") in loader.applied_migrations
        except DatabaseError:  # pragma: no cover
            # errors can happen if database does not exist yet
            return False
