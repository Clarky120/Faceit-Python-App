import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

auth_key = os.getenv("faceit_server_key")
base_url = "https://open.faceit.com"


class FaceitStats:
    def user_stats(nickname):
        player_url = "{}/data/v4/players?nickname={}".format(base_url, nickname)
        player_res = FaceitStats.get_req(full_url=player_url)
        player_info = json.loads(player_res.content)

        stats_url = "{}/data/v4/players/{}/games/cs2/stats".format(
            base_url, player_info["player_id"]
        )

        match_res = FaceitStats.get_req(stats_url)
        match_stats = FaceitStats.match_parser(
            json.loads(match_res.content.decode("utf-8"))["items"]
        )
        return match_stats

    def match_parser(match_array):
        if len(match_array) > 0:
            kills = 0
            deaths = 0
            hs_percentage = 0
            map_dict = {}

            for match in match_array:
                kills += int(match["stats"]["Kills"])
                deaths += int(match["stats"]["Deaths"])
                hs_percentage += int(match["stats"]["Headshots %"])
                if match["stats"]["Map"] in map_dict:
                    map_dict[match["stats"]["Map"]]["won"] += int(match["stats"]["Result"])
                    map_dict[match["stats"]["Map"]]["played"] += 1
                else:
                    map_dict[match["stats"]["Map"]] = {
                        "played": 1,
                        "won": int(match["stats"]["Result"]),
                    }

            average_kills = kills / len(match_array)
            average_deaths = deaths / len(match_array)
            average_hs_percentage = hs_percentage / len(match_array)

            return {
                "kills": average_kills,
                "deaths": average_deaths,
                "hs": average_hs_percentage,
                "maps": FaceitStats.map_parser(map_dict),
            }
    
    def map_parser(map_dict):
        parsed_maps = {}

        for map in map_dict:
            parsed_maps[map] = {
                "played": map_dict[map]["played"],
                "win %": (100 / map_dict[map]["played"]) * map_dict[map]["won"]
            }
        
        return parsed_maps

    def get_req(full_url):
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer {}".format(auth_key),
        }
        res = requests.get(full_url, headers=headers)

        if res.status_code == 200:
            return res
        else:
            raise Exception("Get request failed")
