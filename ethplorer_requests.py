import json
import requests

###############################
#   	ETHPLORER REQUESTS    #
###############################
def get_top_holders():
    return json.loads(requests.get(
       f"https://api.ethplorer.io/getTopTokenHolders/0xAEcc217a749c2405b5ebC9857a16d58Bdc1c367F?apiKey=freekey&limit=100" 
    ).text)["holders"]