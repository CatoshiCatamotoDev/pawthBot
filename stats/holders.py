
import json
from operator import iconcat
import pandas as pd 
import matplotlib.pyplot as plt
from utils import *
import sys 
sys.path.append('..')
from icons import *
from utils.utils import *

ADDR_GRUMPYSWAP = '0x405715ab97d667BE039396adbC99B440d327FEbb'
ADDR_UNISWAP = '0x800A45f2b861229d59E952aeF57B22e84Ff949A1'
ADDR_CHARITY = '0xf4A22C530e8cC64770C4eDb5766D26F8926E20bd'
ADDR_SHIBASWAP = '0xC57dC778A0d2d150d04fC0FD09a0113Ebe9d600c'
ADDR_RADIOSWAP = '0x54a0baF656FCDc383A7c129751742FeCd4eEe726'
ADDR_BSC_BRIDGE = '0xDfed31E640b7280F76f046a97179E5E369D209b5'
ADDR_BIGONE = '0xD4Dcd2459BB78d7a645Aa7E196857D421b10D93F'
ADDR_DEVWALLET = "0x16b1db77b60c8d8b6ecea0fa4e0481e9f53c9ba1"
ADDR_BIGONE = "0xd4dcd2459bb78d7a645aa7e196857d421b10d93f"
ADDR_PANCAKESWAP = '0x0bAbbB875C4eeC2c3F3Fc7936Ec9632fdCE1fAC4'
ADDR_CH2 = '0x409e215738E31d8aB252016369c2dd9c2008Fee0'
ADDR_DEAD = '0x000000000000000000000000000000000000dead'

grumpyswap =  0
shiba_buy = 0
shiba_sell = 0
rad_buy = 0
rad_sell = 0
uni_buy = 0
uni_sell = 0
charity_in = 0
charity_out = 0
any_bsc_to_eth = 0
any_eth_to_bsc = 0
bigone_to = 0
bigone_from = 0

pancake_buy = 0
pancake_sell = 0
bsc_charity_in = 0
bsc_charity_out = 0
transfers = 0
tmp = 0
highest_value_pawth_buy = 0
highest_value_pawth_sell = 0

def transfer_investigate(transfer, txhash):
    # print(transfer)
    # print(transfer['from'])
    global grumpyswap
    global shiba_buy, shiba_sell, uni_buy, uni_sell, rad_buy, rad_sell
    global charity_in, charity_out, bsc_charity_in, bsc_charity_out
    global any_bsc_to_eth, any_eth_to_bsc
    global bigone_from, bigone_to
    global pancake_buy, pancake_sell
    global transfers
    global tmp ##REMOVEME

    global highest_value_pawth_buy, highest_value_pawth_sell
    tx_id = txhash
    value_pawth = (transfer["value"]/1e9)
    # print(value_pawth)

    if(transfer["from"] == ADDR_GRUMPYSWAP):
        grumpyswap = grumpyswap+1
    
    ### Charity wallet (happens every transaction)
    elif(transfer["to"] == ADDR_CHARITY):
        charity_in = charity_in+1
    elif(transfer["from"] == ADDR_CHARITY):
        charity_out = charity_out+1
        
    ### Shibaswap (verified)                    
    elif(transfer["from"] == ADDR_SHIBASWAP):
        print("#####################################")
        print("# SHIBA SELL " + iconShiba + iconCrossMark)
        print("# TX ID = " + str(tx_id))     
        print("#####################################\n") 
        shiba_sell = shiba_sell+1
    elif(transfer["to"] == ADDR_SHIBASWAP):
        print("#####################################")
        print("# SHIBA BUY " + iconShiba + iconGreenCircle)
        print("# TX ID = " + str(tx_id))     
        print("#####################################\n") 
        shiba_buy = shiba_buy+1


    ### Radioswap (verified)                                        
    elif(transfer["from"] == ADDR_RADIOSWAP):
        rad_sell = rad_sell+1         
        print("#####################################")
        print("# RADIO SELL " + iconRadio + iconCrossMark)
        print("# TX ID = " + str(tx_id))     
        print("#####################################\n")   
    elif(transfer["to"] == ADDR_RADIOSWAP):
        rad_buy = rad_buy+1
        print("#####################################")
        print("RADIO BUY " + iconRadio + iconGreenCircle)
        print("# TX ID = " + str(tx_id))     
        print("#####################################\n")

    ### Uniswap (verified)                                        
    elif(transfer["from"] == ADDR_UNISWAP):
        uni_buy = uni_buy+1
        print("#####################################")
        print("# Uniswap Buy " + iconUnicorn + iconGreenCircle)
        print("# TX ID = " + str(tx_id))     
        print("#####################################\n")

    elif(transfer["to"] == ADDR_UNISWAP):
        uni_sell = uni_sell+1
        print("#####################################")
        print("# Uniswap SELL " + iconUnicorn + iconCrossMark)    
        print("# TX ID = " + str(tx_id))     
        print("#####################################\n")
        
    ### Pancakeswap (verified)
    elif(transfer["from"] == ADDR_CH2):
        bsc_charity_out = bsc_charity_out+1
        # print("CHARITY SELL " + iconPancake + iconCrossMark)    
        # print("TX ID = " + str(tx_id))  
        # print("PANCAKE CH " + iconPancake + iconGreenCircle)
    elif(transfer["to"] == ADDR_CH2):
        bsc_charity_in = bsc_charity_in+1
        # print("PANCAKE SELL " + iconPancake + iconCrossMark) 

    elif(transfer["from"] == ADDR_PANCAKESWAP):
        pancake_buy = pancake_buy+1
        
        # print("VALUE = ", str(util_commify(value_pawth)))
        if value_pawth > highest_value_pawth_buy:
            highest_value_pawth_buy = value_pawth

        print("#####################################")
        print("# Pancakeswap BUY " + iconPancake + iconGreenCircle)    
        print("# TX ID = " + str(tx_id))     
        print("#####################################\n")        

    elif(transfer["to"] == ADDR_PANCAKESWAP):
        pancake_sell = pancake_sell+1
        if value_pawth > highest_value_pawth_sell:
            highest_value_pawth_sell = value_pawth
        # print("PANCAKE SELL " + iconPancake + iconCrossMark)    
        print("#####################################")
        print("# Pancakeswap SELL " + iconPancake + iconCrossMark)    
        print("# TX ID = " + str(tx_id))     
        print("#####################################\n")

    ### BSC Bridge (anyswap) (double check!)                                      
    elif(transfer["from"] == ADDR_BSC_BRIDGE):
        any_bsc_to_eth = any_bsc_to_eth+1

    elif(transfer["to"] == ADDR_BSC_BRIDGE):
        any_eth_to_bsc = any_eth_to_bsc+1
        print("ETH TO BSC " + iconBridge + iconGreenCircle)
        # print("BLOCK = " + str(block))
        print("TX ID = " + str(tx_id))  

        
    ### Bigone (verified)                                       
    elif(transfer["from"] == ADDR_BIGONE):
        bigone_from = bigone_from+1
        print("#####################################")
        print("# BIGONE_FROM " + iconOne + iconGreenCircle)    
        print("# TX ID = " + str(tx_id))     
        print("#####################################\n")        

    elif(transfer["to"] == ADDR_BIGONE):
        bigone_to = bigone_to+1                     
        print("#####################################")
        print("# BIGONE_TO " + iconOne + iconCrossMark)    
        print("# TX ID = " + str(tx_id))     
        print("#####################################\n") 
    ### Transfers
    else:
        # The rest are transfers I believe
        transfers = transfers + 1


def transfers_print_stats():
    print("GRUMPYSWAP " + str(grumpyswap))          
    print("SHIBASWAP BUYS " + str(shiba_buy))
    print("SHIBASWAP SELL " + str(shiba_sell))
    print("RADIO BUYS " + str(rad_buy))
    print("RADIO SELL " + str(rad_sell))
    print("UNI BUYS " + str(uni_buy))
    print("UNI SELL " + str(uni_sell))

    print(iconPancake + "PANCAKE BUY " + str(pancake_buy))
    print(iconPancake +"PANCAKE SELL " + str(pancake_sell))
    print(iconPancake + "Highest sell:" + str(util_commify(highest_value_pawth_sell)))
    print(iconPancake + "Highest buy:" + str(util_commify(highest_value_pawth_buy)))

    print("BIGONE TO " + str(bigone_to))
    print("BIGONE FROM " + str(bigone_from))

    print("ETH TO BSC " + str(any_eth_to_bsc))
    print("BSC TO ETH " + str(any_bsc_to_eth))

    print("CHARITY = " + str(charity_in))
    print("CHARITY SELL = " + str(charity_out))
    print(iconPancake + "CHARITY = " + str(bsc_charity_in))
    print(iconPancake + "CHARITY SELL = " + str(bsc_charity_out))

    print(">TRANSFERS = " + str(transfers))

    print("TMP = " + str(tmp))
    sw_total = shiba_buy + shiba_sell + rad_buy + rad_sell + uni_buy + uni_sell + any_eth_to_bsc + any_bsc_to_eth + bigone_to + bigone_from #+ transfers
    
    sw_total += pancake_buy + pancake_sell 
    print("SW TOTAL = " + str(sw_total))


def stats_holders_origin():
    #ETH
    # bl = json.load(open("./transactions-state-eth.json", "rt"))
    
    #BSC
    print(">>>>>>> ")
    bl = json.load(open("./transactions-state-bsc.json", "rt"))
    # print(bl)
    print(bl["last_scanned_block"])
    print(len(bl["blocks"]))

    pairs = bl["blocks"].items()

    #"13403526": 
    #   {
    #       "0x5698b1e28f006ce0b96c0dab538837fe8131001952d157fda9417a11b48fd2c3": 
    #       {"21": 
    #           {"from": "0xC57dC778A0d2d150d04fC0FD09a0113Ebe9d600c", "to": "0xf4A22C530e8cC64770C4eDb5766D26F8926E20bd", "value": 8104306989344, "timestamp": "2021-10-12T12:07:35"}, 
    #        "22": 
    #           {"from": "0xC57dC778A0d2d150d04fC0FD09a0113Ebe9d600c", "to": "0x800A45f2b861229d59E952aeF57B22e84Ff949A1", "value": 389006735488513, "timestamp": "2021-10-12T12:07:35"}
    #       }
    #   }, 
    

    for block, txs in pairs:
        # print(block)
        # print(value)
        # print(value["from"])
        pairs2 = txs.items()
        for tx_id, value2 in pairs2:
            # print(tx_id)
            # print(value2)

            pairs3 = value2.items()
            # print("LEN = " + str(len(value2)))
            # if(len(value2) > 20):
                # print(key2)
                # print(value2)
            for log_id, transfer in pairs3:
                transfer_investigate(transfer, tx_id)

    transfers_print_stats()

    list_of_addresses = []
    list_of_shares = []
    list_of_addresses.append("GRUMPYSWAP")
    list_of_shares.append(grumpyswap)

    list_of_addresses.append("SHIBA")
    list_of_shares.append(shiba_buy)

    list_of_addresses.append("RADIO")
    list_of_shares.append(rad_buy)

    list_of_addresses.append("UNISWAP")
    list_of_shares.append(uni_buy)

    list_of_addresses.append("BIGONE")
    list_of_shares.append(bigone_from)

    # list_of_addresses.append("RADIO")


    colors = ['#f78da7','#fcb900','#9b51e0','#cf2e2e','#0693e3','#8ed1fc']

    labels = list_of_addresses
    shares = list_of_shares

    plt.pie(shares, labels=labels,colors=colors, rotatelabels=45)
    plt.title("Buy distribution overall (ETH Chain)", fontsize=18)
    plt.savefig("holder_origin_pie_chart.png")
    # plt.show()

    return plt
    ## TODO MULTI TRANSFER TRANSACTIONS!!
    # LIKE THIS ONE:
    # https://etherscan.io/tx/0x6e97804d6d22cb204ff4b1f337bda20f179f26698134b3998a3922893205d763





def stats_holders_distribution():

    df = pd.read_json("./holders.json")

    # Specify accounts that are not normal holders


    list_of_accounts_to_exclude = [ADDR_DEAD,ADDR_DEVWALLET,ADDR_UNISWAP,ADDR_BIGONE,ADDR_BSC_BRIDGE]

    # Create lists of all of these addresses, balances, and shares to create your pie chart

    list_of_addresses = []
    list_of_balances = []
    list_of_shares = []
    i = 0


    for holder in df['holders']:
        if holder['address'] == ADDR_DEAD:
            list_of_addresses.append("Burned")
        if holder['address'] == ADDR_UNISWAP:
            list_of_addresses.append("Uniswap")
        if holder['address'] == ADDR_BIGONE:
            list_of_addresses.append("BigOne")
        if holder['address'] == ADDR_BSC_BRIDGE:
            list_of_addresses.append("Bsc Bridge")   
        if holder['address'] == ADDR_DEVWALLET:
            list_of_addresses.append("Dev Wallet")
        if not holder['address'] in list_of_accounts_to_exclude and i <8:
            list_of_addresses.append(holder['address'][0:7])   
        if not holder['address'] in list_of_accounts_to_exclude and i >=8:
            list_of_addresses.append("")   
        list_of_balances.append(holder['balance'])
        list_of_shares.append(holder['share'])
        i +=1

    shares_held_by_people_outside_of_100 = 100 - sum(list_of_shares)
    list_of_addresses.append("Below top 100")
    list_of_shares.append(shares_held_by_people_outside_of_100)


    colors = ['#f78da7','#fcb900','#9b51e0','#cf2e2e','#0693e3','#8ed1fc']

    labels = list_of_addresses
    shares = list_of_shares

    plt.pie(shares, labels=labels,colors=colors, rotatelabels=45)

    # I have this as plt.show(), which simply pulls up the pie chart
    # The plot is in this plt object, so you could save the image as a .png
    plt.savefig("saved_pie_chart.png")
    # plt.show()
    return plt