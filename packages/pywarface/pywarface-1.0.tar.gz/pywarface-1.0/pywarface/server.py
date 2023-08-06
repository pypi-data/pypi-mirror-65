# Each Warface region has it's own set of servers. This allows multiple people
# to have the same username as long as they are playing diffrent servers.
# This file contains the common interface for all servers in the world across
# both "normal" Warface, and Russian Warface.

import requests
from .region import RUSSIA, WORLD, Region
from .userclass import Class
from .user import User
from typing import List
from dataclasses import dataclass


@dataclass
class Server(object):
    """This class contains mappings from the my.com server codenames to their server numbers"""

    # Server data
    server_id: int
    server_codename: str
    region: Region

    def getTop100(self, class_sort: Class = None) -> List[dict]:

        # Build request
        req = {
            "server": self.server_id,
            "class": ""
        }

        # Determine the class parameter
        if class_sort:
            req["class"] = str(class_sort.class_type)

        # Make request to server
        resp = requests.get(
            f"http://api.{self.region.ip_addr}/rating/top100", params=req).json()

        return resp

    def getUser(self, username: str) -> User:

        # Request user info
        resp: dict = requests.get(f"http://api.{self.region.ip_addr}/user/stat", params={
                                  "name": username, "server": self.server_id}).json()

        # Handle errors
        failure = False
        failure |= resp.get("message", "") == "Пользователь не найден"
        failure |= "Ошибка" in resp.get("message", "")

        if failure:
            return None

        # Build user info
        user = User()
        user.uid = resp.get("user_id", "")
        user.nickname = resp.get("nickname", "")
        user.experience = resp.get("experience", 0)
        user.rank = resp.get("rank_id", 0)
        user.clan_id = resp.get("clan_id", -1)
        user.clan_name = resp.get("clan_name", "")
        user.pvp_total_kills = resp.get("kill", 0)
        user.pvp_friendly_kills = resp.get("friendly_kills", 0)
        user.pvp_kills = resp.get("kills", 0)
        user.pvp_deaths = resp.get("death", 0)
        user.pvp_kdr = resp.get("pvp", 0.0)
        user.pve_total_kills = resp.get("pve_kill", 0)
        user.pve_friendly_kills = resp.get("pve_friendly_kills", 0)
        user.pve_kills = resp.get("pve_kills", 0)
        user.pve_deaths = resp.get("pve_death", 0)
        user.pve_kdr = resp.get("pve", 0.0)
        user.playtime = resp.get("playtime", 0)
        user.playtime_hrs = resp.get("playtime_h", 0)
        user.playtime_mins = resp.get("playtime_m", 0)
        user.fav_pvp_class = resp.get("favoritPVP", 0)
        user.fav_pve_class = resp.get("favoritPVE", 0)
        user.pvp_wins = resp.get("pvp_wins", 0)
        user.pvp_losses = resp.get("pvp_lost", 0)
        user.pvp_games_played = resp.get("pvp_all", 0)
        user.pve_wins = resp.get("pve_wins", 0)
        user.pve_losses = resp.get("pve_lost", 0)
        user.pve_games_played = resp.get("pve_all", 0)
        user.pvp_wlr = resp.get("pvpwl", 0.0)

        return user


# Known servers
RU_ALPHA: Server = Server(1, "Alpha", RUSSIA)
RU_BRAVO: Server = Server(2, "Bravo", RUSSIA)
RU_CHARLIE: Server = Server(3, "Charlie", RUSSIA)
ALPHA: Server = Server(1, "Alpha", WORLD)
BRAVO: Server = Server(2, "Bravo", WORLD)

# Parsable list of servers
server_list: list = [RU_ALPHA, RU_BRAVO, RU_CHARLIE,
                     ALPHA, BRAVO]
