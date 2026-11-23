from services.api import find_player,get_player_statistics,APIRequestError


MATCH_FORMATS = {
    "ODI": "odi",
    "Test": "test",
    "T20I": "t20i",
}

def get_player_data(player_name):
    """This function is used to return the players data which we fetched from the api"""

    player_data = find_player(player_name=player_name)

    player_identifier = player_data["player_identifier"]

    player_statistics = get_player_statistics(player_identifier=player_identifier)

    batting = player_statistics.get("data", {}).get("batting", {})

    if not batting:
        raise APIRequestError

    formats = []
    for format_name, api_key in MATCH_FORMATS.items():
        format_stats = batting.get(api_key, {})
        formats.append({
            "name": format_name,
            "matches": format_stats.get("matches", 0),
            "runs": format_stats.get("runs", 0),
        })

    return  {
        "player_name": player_data["player_name"],
        "formats": formats,
    }
