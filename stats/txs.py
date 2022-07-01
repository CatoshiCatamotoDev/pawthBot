
from etherscan_requests import *
from ethplorer_requests import *
from thegraph_requests import *

#Calculate Buy Wall Length
def stats_txs_get_buywall_length():
    statsBuyWallLength = 0
    res = run_query(query_transactions)
    resSwaps = res["data"]["swaps"]
    print(len(resSwaps))
    for i in range(0, len(resSwaps)):
        amount1In = float(resSwaps[i]["amount1In"])
        if(amount1In > 0):
            statsBuyWallLength = statsBuyWallLength + 1
        else:
            break

    return statsBuyWallLength


def stats_txs_get_biggest_buy():
    statsBiggestBuy = 0.0
    res = run_query(query_transactions)
    resSwaps = res["data"]["swaps"]
    
    for i in range(0, len(resSwaps)):
        amount1In = float(resSwaps[i]["amount1In"])
        if(amount1In > statsBiggestBuy):
            statsBiggestBuy = amount1In

    return statsBiggestBuy


def stats_txs_get_biggest_buy2():
    bl = json.load(open("./transactions-state.json", "rt"))
    # print(bl["last_scanned_block"])
    print(len(bl["blocks"]))

    pairs = bl["blocks"].items()
