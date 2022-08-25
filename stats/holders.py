
import json
from operator import iconcat
import pandas as pd 
import matplotlib.pyplot as plt
from utils import *
import sys 
sys.path.append('..')
from icons import *
from utils.utils import *

# ADDR_GRUMPYSWAP = '0x405715ab97d667BE039396adbC99B440d327FEbb'
# ADDR_UNISWAP = '0x800A45f2b861229d59E952aeF57B22e84Ff949A1'
# ADDR_SHIBASWAP = '0xC57dC778A0d2d150d04fC0FD09a0113Ebe9d600c'
# ADDR_RADIOSWAP = '0x54a0baF656FCDc383A7c129751742FeCd4eEe726'
# ADDR_BIGONE = '0xD4Dcd2459BB78d7a645Aa7E196857D421b10D93F'
# ADDR_BSC_BRIDGE = '0xDfed31E640b7280F76f046a97179E5E369D209b5'
# ADDR_DEVWALLET = "0x16b1db77b60c8d8b6ecea0fa4e0481e9f53c9ba1"
# ADDR_PANCAKESWAP = '0x0bAbbB875C4eeC2c3F3Fc7936Ec9632fdCE1fAC4'
# ADDR_SAFEMOON = '0x11b058493cc61691Cae52B6512817c4F913260c2'
# ADDR_DEAD = '0x000000000000000000000000000000000000dead'

ADDR_CHARITY = '0xf4A22C530e8cC64770C4eDb5766D26F8926E20bd'
ADDR_CH2 = '0x409e215738E31d8aB252016369c2dd9c2008Fee0'

contracts_json = json.load(open("settings/settings.json", "rt"))
highest_value_pawth_buy = 0
highest_value_pawth_sell = 0

prices_eth = {}
prices_bnb = {}

def transfer_investigate(transfer, txhash, ch):
    global highest_value_pawth_buy, highest_value_pawth_sell

    msg = ""
    msg2 = ""
    tx_id = txhash
    print("\nTRANSFER INVESTIGATE:")
    print(transfer)
    value_pawth = util_commify(transfer["primaryValue"]/1e6)
    value_other = util_commify(transfer["secondaryValue"]/1e18)
    dex = transfer["dex"]

    print("Pawth = " + str(value_pawth))
    print("Other = " + str(value_other))
    print("Dex = " + dex)

    # value_pawth_orig = transfer["value"]/1e9
    # print(value_pawth)
    # print(transfer["from"])
    # if transfer["from"] != ADDR_GRUMPYSWAP and transfer["from"] != ADDR_UNISWAP and transfer["from"] != ADDR_SHIBASWAP and transfer["from"] != ADDR_RADIOSWAP and transfer["from"] != ADDR_CHARITY:
    #     holders_update(transfer["from"], 1)
    # else:
    #     print(">> IGNORE - " + transfer["from"])

    ts = transfer['timestamp']

    # if amount0In != 0 and amount0Out != 0:
    #     print("ISSUE - TODO")
    #     # Gebeurt bvb hierbij:
    #     #0xd5fceb132b8a32f5e1fc743e1544e940b136ee705770275173b0793c9e2dfc54

    # if amount0In != 0:
    #     value_pawth2 = util_commify(amount0In/1e9)
    # else:
    #     value_pawth2 = util_commify(amount0Out/1e9)


    # if amount1In != 0:
    #     value_eth = round(amount1In/1e18,3)
    # elif amount1Out != 0:
    #     value_eth = round(amount1Out/1e18,3)
    # else:
    #     value_eth = 0
    #     print("ISSUE_TODO")
    # # value_eth = (amount1In/1e18)
    # # value_pawth2 = (amount0Out/1e9)

    #FIX!!
    if transfer["secondaryValue"] != 0:
        price_eth_per_pawth = (transfer["primaryValue"]/1e18)/(transfer["secondaryValue"]/1e6)
    else:
        price_eth_per_pawth = 0

    # if value_pawth != 0:
    #     price_pawth_per_eth = value_eth/value_pawth_orig
    # else:
    #     price_pawth_per_eth = 0
    print("PRICE = " + str(price_eth_per_pawth))
    # print(value_eth)
    c = contracts_json["contracts"]
    j = -1

    for i in range(0, len(c)):
        # print(c[i]["address"])
        if c[i]["ignore"] != 1:
            # print("I = " + str(i))

            # Ignore if a transfer to or from Charity!!
            if transfer["from"] == ADDR_CH2 or transfer["to"] == ADDR_CH2: 
                # print("BSC HARD IGNORE! - " + str(i))
                j = -2
                break
            if transfer["from"] == ADDR_CHARITY or transfer["to"] == ADDR_CHARITY: 
                # print("ETH HARD IGNORE! - " + str(i))
                j = -2
                break

            ########
            ## Check Buys
            ########
            if transfer["dex"] == c[i]["name"]:
                if transfer["type"] == "BUY":
                    # print(transfer)
                    #####
                    # Generate The Message
                    #####
                    msg2 += c[i]["icon"] + "* " + c[i]["name"] + " Buy *" + iconGreenCircle + "_(" + ts + ")_\n"
                    msg2 += "" + str(value_other) + c[i]["paired_with"] + " *<>* " + str(value_pawth) + " PAWTH\n"   
                    msg2 += "" + "[TX](" + c[i]["link_prefix"] + str(tx_id)  + ")\n"

                    msg2 += " > " + str(price_eth_per_pawth) + "PAWTH" + c[i]["paired_with"] + "\n"
###########################
                    # from datetime import datetime
                    # # date_time_str = '18/09/19 01:55:19'
                    # date_time_str = '2022-02-28T18:29:51'
                    # date_time_obj = datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S')

                    #####
                    # Generate Price Info
                    #####
                    ## ETH
                    
                    if ch == 0: # and price_eth_per_pawth > 20000:
                        t = {"price": price_eth_per_pawth, "date": ts}
                        if i != 1:
                            print("NAME =" + c[i]["name"])
                            # print(tx_id)
                            # print(transfer)
                        # print(prices_eth)
                        # print(prices_eth[c[i]["name"]])
                        if t["price"] != 0:
                            prices_eth[c[i]["name"]].append(t)
                        print("APPEND!!")
                        # print(prices_eth)

                    ## BSC
                    if ch == 1 and price_eth_per_pawth > 10000 and price_eth_per_pawth < 500000:
                        t = {"price": price_eth_per_pawth, "date": ts}
                        prices_bnb[c[i]["name"]].append(t)
                    # print(test3)
                    ###############s

                    j = i

                    c[i]["buys"] = c[i]["buys"] + 1
                    # print("BUYS = " + str(c[i]["buys"]))
                    break
            ########
            ## Check Sells
            ########
                elif transfer["type"] == "SELL":
                    msg2 += c[i]["icon"] + "* " + c[i]["name"] + " Sell *" + iconCrossMark + "_(" + ts + ")_\n"
                    msg2 += "" + str(value_pawth) + "PAWTH *<>* " + str(value_other) + c[i]["paired_with"] + "\n"
                    msg2 += "" + "[TX](" + c[i]["link_prefix"] + str(tx_id)  + ")\n"

                    msg2 += " > " + str(price_eth_per_pawth) + "PAWTH/"+ c[i]["paired_with"] + "\n"


                    #####
                    # Generate Price Info
                    #####
                    ## ETH
                    if ch == 0: # and price_eth_per_pawth > 20000:
                        t = {"price": price_eth_per_pawth, "date": ts}
                        if i != 1:
                            print("NAME =" + c[i]["name"])
                            print(tx_id)
                            print(transfer)
                        if t["price"] != 0:
                            prices_eth[c[i]["name"]].append(t)
                        # print(prices_eth)

                    ## BSC
                    if ch == 1 and price_eth_per_pawth > 10000 and price_eth_per_pawth < 500000:
                        t = {"price": price_eth_per_pawth, "date": ts}
                        prices_bnb[c[i]["name"]].append(t)
                    # print(test3)
                    ###############s



                    c[i]["sells"] = c[i]["sells"] + 1

                    j = i
                    break    
                else:
                    print(" >>? TYPE = " + transfer["type"])            
        else:
            # print("IGNORE! - " + str(i))
            continue
        # print(">> MSG:")
        # print(msg2)

    if j == -1:
        # print("TRANSFER!")
        msg2 += iconChain + "*Transfer " + iconChain + "* _(" + ts + ")_\n"
        msg2 += value_pawth + " PAWTH\n" 
        msg2 += "" + transfer["from"] + "* >> *" + transfer["to"] + "\n"

        if ch == 0:
            msg2 += "" + "[TX](https://etherscan.com/tx/" + str(tx_id)  + ")\n"
        else:
            msg2 += "" + "[TX](https://bscscan.com/tx/" + str(tx_id)  + ")\n"


    # if(transfer["from"] == ADDR_GRUMPYSWAP):
    #     grumpyswap = grumpyswap+1
    #     msg += iconGrumpyCat + "* Grumpy Swap" + iconGrumpyCat + "* _(" + ts + ")_\n"
    #     msg += value_pawth + " PAWTH \n" 
    #     msg += "" + "[TX](https://etherscan.com/tx/" + str(tx_id)  + ")\n"
    #     addr_holder = transfer["to"]
    
    # ### Charity wallet (happens every transaction)
    # elif(transfer["to"] == ADDR_CHARITY):
    #     charity_in = charity_in+1
    # elif(transfer["from"] == ADDR_CHARITY):
    #     charity_out = charity_out+1
        
    # ### Shibaswap (verified)                    
    # elif(transfer["from"] == ADDR_SHIBASWAP):
    #     msg += iconShiba + "* SHIBA Sell " + iconCrossMark + "* _(" + ts + ")_\n"
    #     msg += "" + str(value_eth) + "ETH *<>* " + str(value_pawth2) + " PAWTH\n"   
    #     # msg += "# " + str(price_eth_per_pawth) + "PAWTH/ETH")
    #     msg += "" + "[TX](https://etherscan.com/tx/" + str(tx_id)  + ")\n"

    #     shiba_sell = shiba_sell+1
    #     addr_holder = transfer["to"]

    # elif(transfer["to"] == ADDR_SHIBASWAP):
    #     msg += iconShiba + "* SHIBA Buy " + iconGreenCircle + "* _(" + ts + ")_\n"
    #     msg += "" + str(value_pawth2) + "PAWTH *<>* " + str(value_eth) + "ETH\n"
    #     # msg += "# " + str(price_eth_per_pawth) + "PAWTH/ETH")
    #     msg += "" + "[TX](https://etherscan.com/tx/" + str(tx_id)  + ")\n"
    #     shiba_buy = shiba_buy+1
    #     addr_holder = transfer["from"]


    # ### Radioswap (verified)                                        
    # elif(transfer["from"] == ADDR_RADIOSWAP):
    #     rad_sell = rad_sell+1         
    #     msg += iconRadio + "* RADIO Sell " + iconCrossMark + "* _(" + ts + ")_\n"
    #     msg +=  "" + str(value_eth) + "ETH *<>* " + str(value_pawth2) + " PAWTH\n"   
    #     # msg +=  " + str(price_eth_per_pawth) + "PAWTH/ETH"
    #     msg += "" + "[TX](https://etherscan.com/tx/" + str(tx_id)  + ")\n"

    #     addr_holder = transfer["to"]

    # elif(transfer["to"] == ADDR_RADIOSWAP):
    #     rad_buy = rad_buy+1
    #     msg += iconRadio + "* RADIO Buy " + iconGreenCircle + "* _(" + ts + ")_\n"
    #     msg += "" + str(value_pawth2) + " PAWTH *<>* " + str(value_eth) + " ETH"+ "\n"
    #     # msg += "# " + str(price_eth_per_pawth) + "PAWTH/ETH"+ "\n"
    #     msg += "" + "[TX](https://etherscan.com/tx/" + str(tx_id)  + ")\n"

    #     addr_holder = transfer["from"]

    # ### Uniswap (verified)                                        
    # elif(transfer["from"] == ADDR_UNISWAP):
    #     uni_buy = uni_buy+1
    #     msg += iconUnicorn + "* Uniswap Buy " + iconGreenCircle + "* _(" + ts + ")_\n"
    #     msg += "" + str(value_pawth2) + " PAWTH *<>* " + str(value_eth) + " ETH" + "\n"
    #     # msg += "# " + str(price_eth_per_pawth) + "PAWTH/ETH"  + "\n"
    #     msg += "" + "[TX](https://etherscan.com/tx/" + str(tx_id)  + ")\n"
    #     # print(msg)
    #     addr_holder = transfer["to"]

    # elif(transfer["to"] == ADDR_UNISWAP):
    #     uni_sell = uni_sell+1
    #     msg += iconUnicorn + "* Uniswap SELL " + iconCrossMark + "* _(" + ts + ")_\n"
    #     msg += "" + str(value_eth) + "ETH *<>* " + str(value_pawth2) + " PAWTH"+ "\n"
    #     # msg += "# " + str(price_eth_per_pawth) + "PAWTH/ETH"+ "\n"
    #     msg += "" + "[TX](https://etherscan.com/tx/" + str(tx_id)  + ")\n"
    #     # print(msg)
    #     addr_holder = transfer["from"]

    # ### Pancakeswap (verified)
    # elif(transfer["from"] == ADDR_CH2):
    #     bsc_charity_out = bsc_charity_out+1
    #     # print("CHARITY SELL " + iconPancake + iconCrossMark)    
    #     # print("TX ID = " + str(tx_id))  
    #     # print("PANCAKE CH " + iconPancake + iconGreenCircle)
    # elif(transfer["to"] == ADDR_CH2):
    #     bsc_charity_in = bsc_charity_in+1
    #     # print("PANCAKE SELL " + iconPancake + iconCrossMark) 

    # elif(transfer["from"] == ADDR_PANCAKESWAP):
    #     pancake_buy = pancake_buy+1
        
    #     # # print("VALUE = ", str(util_commify(value_pawth)))
    #     # if value_pawth > highest_value_pawth_buy:
    #     #     highest_value_pawth_buy = value_pawth

    #     msg += iconPancake + "* Pancakeswap Buy " + iconGreenCircle + "* _(" + ts + ")_\n"
    #     msg += "" + str(value_eth) + "BSC *<>* " + str(value_pawth2) + " PAWTH"+ "\n"
    #     msg += "" + "[TX](https://bscscan.com/tx/" + str(tx_id)  + ")\n"
    #     addr_holder = transfer["to"]    

    # elif(transfer["to"] == ADDR_PANCAKESWAP):
    #     pancake_sell = pancake_sell+1
    #     # if value_pawth > highest_value_pawth_sell:
    #     #     highest_value_pawth_sell = value_pawth

    #     msg += iconPancake + "*Pancakeswap Sell " + iconCrossMark + "* _(" + ts + ")_\n"
    #     msg += "" + str(value_eth) + "BSC *<>* " + str(value_pawth2) + " PAWTH"+ "\n"
    #     msg += "" + "[TX](https://bscscan.com/tx/" + str(tx_id)  + ")\n"

    #     addr_holder = transfer["from"]

    # elif(transfer["from"] == ADDR_SAFEMOON):
    #     safemoon_buy = safemoon_buy+1
        
    #     # print("VALUE = ", str(util_commify(value_pawth)))
    #     # if value_pawth > highest_value_pawth_buy:
    #     #     highest_value_pawth_buy = value_pawth

    #     msg += iconRocket + "*Safemoon Buy " + iconGreenCircle + "* _(" + ts + ")_\n"  
    #     msg += "" + str(value_eth) + "BSC *<>* " + str(value_pawth2) + " PAWTH"+ "\n"
    #     msg += "" + "[TX](https://bscscan.com/tx/" + str(tx_id)  + ")\n"


    #     addr_holder = transfer["to"]    

    # elif(transfer["to"] == ADDR_SAFEMOON):
    #     safemoon_sell = safemoon_sell+1
    #     # if value_pawth > highest_value_pawth_sell:
    #     #     highest_value_pawth_sell = value_pawth
    #     msg += iconRocket + "*Safemoon SELL " + iconCrossMark + "* _(" + ts + ")_\n"
    #     msg += "" + str(value_eth) + "BSC *<>* " + str(value_pawth2) + " PAWTH"+ "\n"
    #     msg += "" + "[TX](https://bscscan.com/tx/" + str(tx_id)  + ")\n"
        

    #     print(">>>>>>>>>>>>>><<<<<<<<<<<<<<<<")
    #     print(tx_id)
    #     print(transfer)
    #     addr_holder = transfer["from"]

    # ### BSC Bridge (anyswap) (double check!)                                      
    # elif(transfer["from"] == ADDR_BSC_BRIDGE):
    #     any_bsc_to_eth = any_bsc_to_eth+1
    #     addr_holder = transfer["to"]

    # elif(transfer["to"] == ADDR_BSC_BRIDGE):
    #     any_eth_to_bsc = any_eth_to_bsc+1
    #     print("ETH TO BSC " + iconBridge + iconGreenCircle)
    #     # print("BLOCK = " + str(block))
    #     print("TX ID = " + str(tx_id))  
    #     addr_holder = transfer["from"]

        
    # ### Bigone (verified)                                       
    # elif(transfer["from"] == ADDR_BIGONE):
    #     bigone_from = bigone_from+1
    #     print("#####################################")
    #     print("# BIGONE_FROM " + iconOne + iconGreenCircle)    
    #     print("# TX ID = " + str(tx_id))     
    #     print("#####################################\n") 
    #     addr_holder = transfer["to"]       

    # elif(transfer["to"] == ADDR_BIGONE):
    #     bigone_to = bigone_to+1                     
    #     print("#####################################")
    #     print("# BIGONE_TO " + iconOne + iconCrossMark)    
    #     print("# TX ID = " + str(tx_id))     
    #     print("#####################################\n") 
    #     addr_holder = transfer["from"]
    # ### Transfers
    # else:
    #     print(">>TRANSFER")

    #     msg += iconChain + "*Transfer " + iconChain + "* _(" + ts + ")_\n"
    #     msg += value_pawth + " PAWTH\n" 

    #     # print(transfer)

    #     msg += "" + transfer["from"] + "* >> *" + transfer["to"] + "\n"

    #     if ch == 0:
    #         msg += "" + "[TX](https://etherscan.com/tx/" + str(tx_id)  + ")\n"
    #     else:
    #         msg += "" + "[TX](https://bscscan.com/tx/" + str(tx_id)  + ")\n"

    #     # print(transfer["to"])
    #     # print(transfer["from"])
    #     # print("TX ID = " + str(tx_id))  
    #     # The rest are transfers I believe
    #     transfers = transfers + 1
    #     addr_holder = transfer["from"]
    #     addr_holder = transfer["to"]

    # ## HOLDER LIST UPDATE!
    # # if addr_holder != '0x9Dc13931B51f974D8d7D85Af272B4c80E4B0E809':
    # # holders_update(addr_holder, 1, ch)
    # # else:
    # #     print("ME")

    # # print(">>>> MSG:")
    # # print(msg)
    # # print(">>>> MSG2:")
    # # print(msg2)
    return msg2

def transfers_print_stats():
    c = contracts_json["contracts"]
    j = -1
    for i in range(0, len(c)-1):
        print(c[i]["icon"] + " " + c[i]["name"] + " - buys: " + str(c[i]["buys"]) + ", sells = " + str(c[i]["sells"]))

    # print("GRUMPYSWAP " + str(grumpyswap))          
    # print("SHIBASWAP BUYS " + str(shiba_buy))
    # print("SHIBASWAP SELL " + str(shiba_sell))
    # print("RADIO BUYS " + str(rad_buy))
    # print("RADIO SELL " + str(rad_sell))
    # print("UNI BUYS " + str(uni_buy))
    # print("UNI SELL " + str(uni_sell))

    # print(iconPancake + "PANCAKE BUY " + str(pancake_buy))
    # print(iconPancake +"PANCAKE SELL " + str(pancake_sell))
    # print(iconPancake + "Highest sell:" + str(util_commify(highest_value_pawth_sell)))
    # print(iconPancake + "Highest buy:" + str(util_commify(highest_value_pawth_buy)))

    # print(iconRocket + "SAFEMOON BUY " + str(safemoon_buy))
    # print(iconRocket +"SAFEMOON SELL " + str(safemoon_sell))
    # print("BIGONE TO " + str(bigone_to))
    # print("BIGONE FROM " + str(bigone_from))

    # print("ETH TO BSC " + str(any_eth_to_bsc))
    # print("BSC TO ETH " + str(any_bsc_to_eth))

    # print("CHARITY = " + str(charity_in))
    # print("CHARITY SELL = " + str(charity_out))
    # print(iconPancake + "CHARITY = " + str(bsc_charity_in))
    # print(iconPancake + "CHARITY SELL = " + str(bsc_charity_out))

    # print(">TRANSFERS = " + str(transfers))

    # print("TMP = " + str(tmp))
    # sw_total = shiba_buy + shiba_sell + rad_buy + rad_sell + uni_buy + uni_sell + any_eth_to_bsc + any_bsc_to_eth + bigone_to + bigone_from #+ transfers
    
    # sw_total += pancake_buy + pancake_sell  + safemoon_buy + safemoon_sell
    # print("SW TOTAL = " + str(sw_total))


def stats_holders_origin():
   
   ####
   # Check all transactions on ETH
   ####
    bl = json.load(open("./tx_radio_usdc-1.json", "rt"))

#     # print(bl)
#     # print(bl["last_scanned_block"])
#     # print(len(bl["blocks"]))
    c = contracts_json["contracts"]

    for i in range(0, len(c)):
        if c[i]["chain"] == "ETH":
            prices_eth[c[i]["name"]] = []
        elif c[i]["chain"] == "BSC":
            prices_bnb[c[i]["name"]] = []
        else:
            print("!!ISSUE!!")
    pairs = bl["blocks"].items()

#     #"13403526": 
#     #   {
#     #       "0x5698b1e28f006ce0b96c0dab538837fe8131001952d157fda9417a11b48fd2c3": 
#     #       {"21": 
#     #           {"from": "0xC57dC778A0d2d150d04fC0FD09a0113Ebe9d600c", "to": "0xf4A22C530e8cC64770C4eDb5766D26F8926E20bd", "value": 8104306989344, "timestamp": "2021-10-12T12:07:35"}, 
#     #        "22": 
#     #           {"from": "0xC57dC778A0d2d150d04fC0FD09a0113Ebe9d600c", "to": "0x800A45f2b861229d59E952aeF57B22e84Ff949A1", "value": 389006735488513, "timestamp": "2021-10-12T12:07:35"}
#     #       }
#     #   }, 
    
    ch = 0
    for block, txs in pairs:
        # print(block)
        # print(value)
        # print(value["from"])
        pairs2 = txs.items()
        for tx_id, transfer in pairs2:
            print(tx_id)
            print(transfer)
            transfer_investigate(transfer, tx_id, ch)
            
    # bl = json.load(open("./transactions-state-bsc.json", "rt"))
    # # # print(bl)
    # # # print(bl["last_scanned_block"])
    # # # print(len(bl["blocks"]))


    # # ####
    # # # Check all transactions on BSC
    # # ####

    # pairs = bl["blocks"].items()

    # ch = 1
    # for block, txs in pairs:
    #     # print(block)
    #     # print(value)
    #     # print(value["from"])
    #     pairs2 = txs.items()
    #     for tx_id, value2 in pairs2:
    #         # print(tx_id)
    #         # print(value2)

    #         pairs3 = value2.items()
    #         # print("LEN = " + str(len(value2)))
    #         # if(len(value2) > 20):
    #             # print(key2)
    #             # print(value2)
    #         for log_id, transfer in pairs3:
    #             # print(transfer)
    #             transfer_investigate(transfer, tx_id, ch)





    transfers_print_stats()
    # print(test3)
    # print(len(test3))
    #TODO: holders_save -> json_save or so...
    print(prices_eth)
    print("SAAAAVE")
    holders_save(prices_eth, "prices_radio_usdc.json")
    # holders_save(prices_bnb, "prices_tmp2.json")

    # list_of_addresses = []
    # list_of_shares = []
    # c = contracts_json["contracts"]
    # j = -1
    # for i in range(0, len(c)-1):

    #     # print(c[i]["icon"] + " " + c[i]["name"] + " - buys: " + str(c[i]["buys"]) + ", sells = " + str(c[i]["sells"]))
    #     if c[i]["ignore"] != 1:
    #         list_of_addresses.append(c[i]["name"])
    #         list_of_shares.append(c[i]["buys"])

    # colors = ['#f78da7','#fcb900','#9b51e0','#cf2e2e','#0693e3','#8ed1fc', '#1234567']

    # labels = list_of_addresses
    # shares = list_of_shares

    # plt.pie(shares, labels=labels,colors=colors, rotatelabels=45)
    # plt.title("Buy distribution overall (ETH + BSC Chain)", fontsize=18)
    # plt.savefig("holder_origin_pie_chart.png")
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


def stats_holders_ranking(address):

    df = pd.read_json("./holders_new.json")
    # print(df)
    i = 0
    for test in df['holders']:
        i = i+1
        # print(test)
        if test['address'] == address:
            print(i)
            print("BINGO!")
            value = test['value']
            return i, value

    return -1

def stats_holders_count():

    df = pd.read_json("./holders_new.json")
    # print(df)
    i = 0
    for test in df['holders']:
        # i = i+1
        # print(test)
        value = test['value']

        if value > 0:
            i = i+1

    print ("I ==== " + str(i))



    # df = pd.read_json("./holders_bsc.json")
    # # print(df)
    # i = 0
    # for test in df['holders']:
    #     # i = i+1
    #     # print(test)
    #     value = test['value']

    #     if value > 0:
    #         i = i+1

    # return -1
    return i



def stats_holders_whale_dominance():
    msg = ""

    data = pd.read_json("./holders_new.json")
    h = data["holders"]
    holder0 = h[0]
    holder1 = h[1]
    holder2 = h[2]
    holder3 = h[3]
    holder10 = h[10]
    holder20 = h[20]
    holder50 = h[50]
    holder100 = h[99] #take 99 as we only get 100 values from ethplorer


    sumDominance = 0
    for i in range(1,3):
        sumDominance += int(h[i]['value'])        
    msg += " Top 3: " + str(round(sumDominance/1e18*100,2)) + " %\n"
    for i in range(4,10):
        sumDominance += int(h[i]['value'])        
    msg += " Top 10: " + str(round(sumDominance/1e18*100,2)) + "%\n"

    for i in range(11,50):
        sumDominance += int(h[i]['value'])        
    msg += " Top 50: " + str(round(sumDominance/1e18*100,2)) + "%\n"

    for i in range(51,99):
        sumDominance += int(h[i]['value'])  
    msg += " Top 100: " + str(round(sumDominance/1e18*100,2)) + "%\n"
    print(msg)
    return msg

def stats_holders_thresholds():
    msg = ""

    data = pd.read_json("./holders_new.json")
    h = data["holders"]
    holder0 = h[0]
    print(holder0)
    holder1 = h[1]
    holder2 = h[2]
    holder3 = h[3]
    holder10 = h[10]
    holder20 = h[20]
    holder50 = h[50]
    holder100 = h[100] #take 99 as we only get 100 values from ethplorer

    msg += "\n > top 3: " + str(util_commify(holder3['value']/1e9)) + " (" + str(round(holder3['value']/1e18*100,2)) +"%)"
    msg += "\n > top 10: " + str(util_commify(holder10['value']/1e9)) + " (" + str(round(holder10['value']/1e18*100,2)) +"%)"
    msg += "\n > top 50: " + str(util_commify(holder50['value']/1e9)) + " (" + str(round(holder50['value']/1e18*100,2)) +"%)"
    msg += "\n > top 100: " + str(util_commify(holder100['value']/1e9)) + " (" + str(round(holder100['value']/1e18*100,2)) +"%)"

    msg += "\n\nNote: the dead/burn wallet holds 14.2% " + iconFire +"\n"

    print(msg)
    return msg





def stats_my_transactions(address):
    bl = json.load(open("./transactions-state-eth.json", "rt"))
    pairs = bl["blocks"].items()
    
    ch = 0
    msg = ""
    msg += "``` === ETHEREUM === ```\n"
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
                # print(transfer)
                if transfer["from"] == address:
                    print("BINGO 1!!! - " + tx_id)
                    msg += transfer_investigate(transfer, tx_id, ch)
                    print(msg)

                if transfer["to"] == address:
                    print("BINGO 2!!! - " + tx_id)
                    msg += transfer_investigate(transfer, tx_id, ch)
                    print(msg)



    bl = json.load(open("transactions-state-bsc.json", "rt"))
    pairs = bl["blocks"].items()
    ch = 1

    msg += "```\n\n === BINANCE SMART CHAIN === ```\n"

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
                # print(transfer)
                if transfer["from"] == address:
                    print("BINGO 1!!! - " + tx_id)
                    msg += transfer_investigate(transfer, tx_id, ch)
                    print(msg)

                if transfer["to"] == address:
                    print("BINGO 2!!! - " + tx_id)
                    msg += transfer_investigate(transfer, tx_id, ch)
                    print(msg)             

    return msg

#######
#   GENERATE HOLDERS.JSON LIST
#######

import ast
import time
import random
import csv
from tempfile import NamedTemporaryFile
import shutil
import threading
from time import sleep
import sys
from scan_transactions import *

test = {}
# test2 = {}
def holders_save(test2, filename):
    """Save everything we have scanned so far in a file."""
    with open(filename, "wt") as f:
        json.dump(test2, f)
    # test.last_save = time.time()


def holders_load(filename):
    """Restore the last scan state from a file."""
    try:
        # print("LOAD")
        test2 = json.load(open(filename, "rt"))
        # print(test2)
        # print(f"Restored the state, previously {self.state['last_scanned_block']} blocks have been scanned")
    except (IOError, json.decoder.JSONDecodeError):
        print("State starting from scratch")
        # self.reset()

    return test2


def holders_update(id, value, chain):
    filename = 'holders_all.json'

    print("HOLDERS UPDATE")
    test2 = holders_load(filename)

    # print(filename)

    # print(">>"+ id)
    # cntEth = 0
    # cntBsc = 0
    # for i in range(0, len(test2["holders"])-1):
    #     if test2["holders"][i]["balanceBsc"]  > 940118252890520:
    #         if test2["holders"][i]["balanceEth"]  > 940118252890521:
    #             cntBsc = cntBsc + 1
    #     if test2["holders"][i]["balanceEth"]  > 1000:
    #         cntEth = cntEth + 1



    # print("cntEth = " + str(cntEth))
    # print("cntBsc = " + str(cntBsc))

    j = -1    
    for i in range(0, len(test2["holders"])-1):
        # print(i)
        # print(test2["holders"][i]["address"])
        # if("address" in test2["holders"][i]):
        if test2["holders"][i]["address"] == str(id):
            print("BINGO")
            j = i
            break
        # else:
            # print("NOPE")

    # If we have a balance, don't recheck.
    # NOTE: risk that a balance has changed and not rechecked...
    if j == -1:
        # if chain == 0:
        balBsc=getBalance(0x9Dc13931B51f974D8d7D85Af272B4c80E4B0E808, API_URL_ETH, id, 0)
        # else:
        balEth=getBalance(0x9Dc13931B51f974D8d7D85Af272B4c80E4B0E808, API_URL_BSC, id, 1)

        t = {"address": id, "balanceEth": 0, "balanceBsc": 0, "transactions": 0}
        test2["holders"].append(t)
        tt = test2["holders"][len(test2["holders"]) - 1]

        #  Update balance
        # if chain == 0:
        tt["balanceEth"] = balEth
        # else:
        tt["balanceBsc"] = balBsc

    else:         
        print("FOUND: " + str(j))
        tt = test2["holders"][j]




    tt["transactions"] = tt["transactions"] + 1
    # print(">>")
    test2["last_scanned_block"] = 0

    holders_save(test2, filename)
    print("HOLDERS UPDATE DONE - len=" + str(len(test2["holders"])))

    # newFile = NamedTemporaryFile('w+t', newline='', delete=False)
    # with open (filename, "r", newline='') as origFile, newFile:
    #     fields=['userAddress', 'userValue', 'share', 'transfers']

    #     sortlist=[]
    #     reader=csv.reader(origFile)
    #     writer=csv.writer(newFile) 
    #     # writer.writerow({'userAddress' : id, 'userValue' : value, 'userShare' : userShare})


    #     for i in reader:
    #         sortlist.append(i)

    #     # print(sortlist)
    #     userFound = False
    #     #Check if the userAddress is found. If so, increase its userShare.
    #     # If not, add to the list and set at userShare of 1
    #     for i in range(1, len(sortlist)):
    #         # sortlist[i][0]=int(sortlist[i][int(0)], 0)
    #         # sortlist[i][2]=int(sortlist[i][int(2)], 0)
    #         # print("\n\n>>>>")
    #         # print(sortlist[i][0])
    #         if int(sortlist[i][0], 0) == int(id, 0):
    #             sortlist[i][1] = bal
    #             sortlist[i][3] = int(sortlist[i][3]) + 1
    #             userFound = True
    #             print("USER FOUND!!" + hex(int(id, 0)))

    #     #User not found. Append
    #     if userFound == False:
    #         print("User NOT found!!")
    #         testrow = [id, bal, 0, 1]
    #         sortlist.append(testrow)
            
    #     # Now sort the list based on the value of Pawth (the second column)
    #     # sorted_scores = sorted(sortlist, key= lambda x: x[2], reverse=True)


    #     #  Write the sorted list to a new (temporary) file.
    #     for i in range(len(sortlist)):
    #         newstr=[sortlist[i][0], sortlist[i][1], sortlist[i][2], sortlist[i][3]]
    #         writer.writerow(newstr)           

    # # Replace the old file with the new one
    # shutil.move(newFile.name, filename)


    # holders_save(self)
    # # return sorted_scores


