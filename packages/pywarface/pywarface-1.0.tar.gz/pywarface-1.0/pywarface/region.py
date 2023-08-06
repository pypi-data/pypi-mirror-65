# There are technically two diffrent versions of Warface.
# One is Russia-only, the other is for the rest of the world.
# As far as I know, the games are mostly the same gameplay-wise,
# but they physically use diffrent sets of servers, and have
# seprate API endpoints (and even account databases)

from dataclasses import dataclass


@dataclass
class Region(object):
    """This class contains info for each region"""

    # Class data
    ip_addr: str
    name: str


# Known regions
RUSSIA: Region = Region("warface.ru", "Russia")
WORLD: Region = Region("wf.my.com", "World")

# List for easy parsing
region_list: list = [WORLD, RUSSIA]
