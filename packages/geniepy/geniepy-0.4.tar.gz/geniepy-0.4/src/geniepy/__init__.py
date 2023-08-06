"""GeniePy Package entry point."""
from pkg_resources import get_distribution, DistributionNotFound
from geniepy.pubmed_historical import spawn_processes, parse_pubmed_article_set

try:
    # Change here if project is renamed and does not equal the package name
    DIST_NAME = __name__
    __version__ = get_distribution(DIST_NAME).version
except DistributionNotFound:
    __version__ = "unknown"
finally:
    del get_distribution, DistributionNotFound

__author__ = "The Harvard LAMP Team"
__copyright__ = "The Harvard LAMP Team"
__license__ = "MIT"


__all__ = ["parse_pubmed_article_set", "spawn_processes"]
