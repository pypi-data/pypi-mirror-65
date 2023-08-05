import logging
import subprocess
from functools import lru_cache

log = logging.getLogger(__name__)


class Metadata:
    def __init__(self, *, namespace, name, description=None, title=None, **info):
        self.namespace = namespace
        self.name = name
        self.description = description
        self.title = title or f"{namespace}/{name}"
        self.info = info
        self.version = read_version()


@lru_cache(maxsize=1)
def read_version():
    """Attempts to read the version from the environment, returning 'NA' when it
    fails.  It first looks for the existence of a VERSION file, then tries to
    use git to obtain a tag.

    :returns: A string describing the version.
    """
    return _read_version_from_file() or _read_version_from_git() or "NA"


def _read_version_from_file():
    handle = None
    try:
        log.info("Reading version from file")
        handle = open("VERSION", "r")
        return handle.read().rstrip()
    except FileNotFoundError:
        return None
    finally:
        if handle:
            handle.close()


def _read_version_from_git():
    try:
        return (
            subprocess.run(
                ["git", "describe", "--always", "--tags"], stdout=subprocess.PIPE
            )
            .stdout.decode("utf-8")
            .rstrip()
        )
    except subprocess.SubprocessError:
        return None
    except FileNotFoundError:
        return None
