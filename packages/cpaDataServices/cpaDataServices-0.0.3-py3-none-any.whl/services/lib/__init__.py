"""
This is a init python file.

This helps build the python package for distro.
"""
# Standard Python Libraries
from datetime import datetime
import os

# Third-Party Libraries
from pkg_resources import DistributionNotFound, get_distribution

try:
    _dist = get_distribution("cpaDataServices")
    # Normalize case for Windows systems
    dist_loc = os.path.normcase(_dist.location)
    here = os.path.normcase(os.path.abspath(__file__))
    if not here.startswith(os.path.join(dist_loc, "lib")):
        # not installed, but there is another version that *is*
        raise DistributionNotFound
except DistributionNotFound:
    __version__ = "could not get version from pkg_resources, install this!"
else:
    __version__ = _dist.version

install_date = datetime.fromtimestamp(os.path.getmtime(__file__))
