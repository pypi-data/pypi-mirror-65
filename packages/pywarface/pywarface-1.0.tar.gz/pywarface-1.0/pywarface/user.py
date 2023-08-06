from dataclasses import dataclass


@dataclass(init=False)
class User:
    """All info about a user"""

    # User stats
    uid: str
    nickname: str
    experience: int
    rank: int
    clan_id: int
    clan_name: str
    pvp_total_kills: int
    pvp_friendly_kills: int
    pvp_kills: int
    pvp_deaths: int
    pvp_kdr: float
    pve_total_kills: int
    pve_friendly_kills: int
    pve_kills: int
    pve_deaths: int
    pve_kdr: float
    playtime: int
    playtime_hrs: int
    playtime_mins: int
    fav_pvp_class: str
    fav_pve_class: str
    pvp_wins: int
    pvp_losses: int
    pvp_games_played: int
    pve_wins: int
    pve_losses: int
    pve_games_played: int
    pvp_wlr: float

    # Plaintext stat data
    # This contains a lot more info that I don't think
    # is worth parsing. If anyone needs it, it is here
    raw_stats: str
