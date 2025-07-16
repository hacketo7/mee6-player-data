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
            players = resp.json().get("players", []) # convert the json into a python dict in the form. if its not a json return a empty dict
            # explanation of the dict
            """{'avatar': '', 'discriminator': '', 'guild_id': '', 'id': '', 'message_count': , 'monetize_xp_boost': , 'username': '', 'xp': , 'is_monetize_subscriber': , 'detailed_xp': , 'level': }
                avatar: a hash of the player id's profile picture.
                discriminator: the old discord # next to your name. this is always 0 now since discord removed it.
                guild id: the server id you provided. 
                message_count: the total number of messages THAT earned xp in the server id.
                monetize_xp_boost: the xp boost for subscribing to mee6. (0 if not subscribed)
                username: the username of the player id.
                xp: the total all time xp EARNED in the server id.
                is_monetize_subscriber: True if you subscribed to MEE6, False if not
                detailed_xp: returns 3 numbers in a list ([])

                # detailed xp explanation
                
                the first number is the XP EARNED in that current level in the server id.
                the second number is the XP NEEDED to reach the next level in the server id.
                the third number is the TOTAL XP earned in the server id. (same as xp)
            """
        except requests.exceptions.HTTPError as err:
            return err.response.text
        except requests.exceptions.JSONDecodeError as err:
            return "invalid json"

        for p in players: # checking for the player
            if p["id"] == player_id:
                return p

        if not players: # if the player id wasn't found in any of the pages
            return None

        await asyncio.sleep(0.5) # delay 500ms or you will be temporarily ip blocked
