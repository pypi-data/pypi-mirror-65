from __future__ import annotations

from atomic_write_path import atomic_write_path

from ._version import get_versions


__all__ = ["atomic_write_path"]
__version__ = get_versions()["version"]
del get_versions
