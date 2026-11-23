
import requests
import logging
from config import Config

logger = logging.getLogger(__name__)

class PlayerNotFoundError(Exception):
    pass

class APIRequestError(Exception):
    pass

def find_player(player_name):
    """This function used to fing whether player exist in api or not and returns player's identifier and name"""
    if not player_name or not player_name.strip():
        raise ValueError("Player Name cannot be empty.")

    search_url = f"{Config.API_BASE_URL}{Config.SEARCH_ENDPOINT}"

    params = {
        "q":player_name.strip()
    }
    try:
        response = requests.get(url=search_url,params=params,headers=Config.API_HEADERS,timeout=Config.API_TIMEOUT)
        response.raise_for_status()
        player_info = response.json()
    except requests.exceptions.RequestException as error:
        logger.exception("Player Search API request failed")
        raise APIRequestError("Unable to connect to API request.") from error


    players = player_info.get("data",{}).get("players",[])

    if not players:
        raise PlayerNotFoundError("Player Not Found.")

    player = players[0]
    player_identifier = player.get("player")
    found_player_name = player.get("name")

    if not player_identifier or not found_player_name:
        raise APIRequestError("Player information is incomplete.")

    return {"player_identifier":player_identifier,
            "player_name":player_name
            }



def get_player_statistics(player_identifier):
    """This function is used to retrieve data from the api based on identfier"""

    if not player_identifier:
        raise ValueError("Player Identifier cannot be empty.")
    try:
        stats_endpoint = Config.STATS_ENDPOINT.format(player_identifier=player_identifier)
        stats_url = f"{Config.API_BASE_URL}{stats_endpoint}"
        stat_response = requests.get(url=stats_url,headers=Config.API_HEADERS,timeout=Config.API_TIMEOUT)
        stat_response.raise_for_status()
        player_stats = stat_response.json()
    except requests.exceptions.RequestException as error:
        logger.exception("Statistics API request failed.")
        raise APIRequestError("Unable to retrieve player statistics.") from error

    return player_stats


