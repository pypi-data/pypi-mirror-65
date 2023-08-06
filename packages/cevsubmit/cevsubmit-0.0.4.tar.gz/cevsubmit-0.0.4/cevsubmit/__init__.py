from pkg_resources import get_distribution, DistributionNotFound
import os

# https://stackoverflow.com/questions/17583443/what-is-the-correct-way-to-share-package-version-with-setup-py-and-the-package
try:
    _dist = get_distribution("cevsubmit")
    # Normalize path for cross-OS compatibility.
    _dist_loc = os.path.normcase(_dist.location)
    _here = os.path.normcase(__file__)
    if not _here.startswith(os.path.join(_dist_loc, "cevsubmit")):
        # This version is not installed, but another version is.
        raise DistributionNotFound
except DistributionNotFound:
    __version__ = "locally installed, no version information available"
else:
    __version__ = _dist.version

CONFIG_LOADER = __import__("lib50").config.Loader("cevsubmit")
CONFIG_LOADER.scope("files", "include", "exclude", "require")
