###############################
#   	ETHERSCAN REQUESTS    #
###############################
def get_last_block(since):
    result = int(json.loads(requests.get(
        f"https://api.etherscan.io/api?module=block&action=getblocknobytime&timestamp={round(time.time() - since)}&closest=before&apikey={ETHERSCAN_API_KEY}"
    ).text)["result"])

    print(result)
    return result
    #Note: we need action = txlist and 'contractaddress' instead of 'address'!!

def get_last_txs(since=86400):
    print(since)
    return json.loads(requests.get(
        f"https://api.etherscan.io/api?module=account&action=tokentx&contractaddress={TOKEN_ADDRESS}&startblock={get_last_block(since)}&endblock=999999999&sort=asc&apikey={ETHERSCAN_API_KEY}"
    ).text)["result"] 



def get_tx_info(txhash):
    return json.loads(requests.get(
       f"https://api.etherscan.io/api?module=proxy&action=eth_getTransactionByHash&txhash={txhash}&apikey={ETHERSCAN_API_KEY}" 
    ).text)["result"] 

def get_eth_value():
    return json.loads(requests.get(
       f"https://api.etherscan.io/api?module=stats&action=ethprice&apikey={ETHERSCAN_API_KEY}" 
    ).text)["result"] 
