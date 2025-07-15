# libs
import requests
import asyncio

# mee6 data fetch
async def fetch_player_data(server_id, player_id):
    page = -1 # each page has 100 users and it starts from 0
    url = f"https://mee6.xyz/api/plugins/levels/leaderboard/{server_id}" # unofficial mee6 api for leaderboard of server_id
    while True:
        page += 1 
        try:
            resp = requests.get(url=url, params={"page": page}) # returns a json of the page of 100 users
            resp.raise_for_status() # breaks code if its a 400 or 500 error
            players = resp.json().get("players", []) # convert the json into a python dict. if its not a json return a empty dict
        except requests.exceptions.HTTPError as err:
            return err.response.text
        except requests.exceptions.JSONDecodeError as err:
            return "invalid json"

        for p in players: # checking for the player
            if p["id"] == player_id:
                return p

        if not players: # if the player id wasn't found in any of the pages
            return None

        await asyncio.sleep(0.5) # delay 500ms
