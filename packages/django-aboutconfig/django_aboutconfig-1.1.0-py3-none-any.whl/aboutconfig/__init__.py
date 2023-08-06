"""A firefox-like about:config implementation for one-off settings in Django apps."""

from typing import Any


__version__ = (1, 1, 0)
default_app_config = "aboutconfig.apps.AboutconfigConfig"  # pylint: disable=invalid-name


def get_config(key: str, value_only: bool = True) -> Any:
    """Get configured value by key.

    By default returns value only. If ``value_only`` is ``False``, returns an instance of
    aboutconfig.utils.DataTuple which also contains the ``allow_template_use`` value.

    This is a lazy wrapper around the internal ``utils.get_config()`` function."""

    from . import utils  # pylint: disable=import-outside-toplevel

    return utils.get_config(key, value_only)
