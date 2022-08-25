#########################
#       Imports         #
#########################
import threading
import time
from time import sleep
import os.path
from stats.holders import *
from stats.txs import *
from telegram.tg import thread_telegram

from utils.utils import *
from etherscan_requests import *
from ethplorer_requests import *

from scan_transactions import *

from icons import *  
from twitter.tweets import *
from telegram.tg import *

# from holders import *
##########################
#   	SETTINGS         #
##########################
VERSION_STR="0.01"


def thread_scan_bsc():
    while True:
        try:
            # scan_run_bsc()
            scan_run_eth()
            time.sleep(20)
        except Exception as e:
                print(e)
                time.sleep(10)


stats_holders_origin()
# stats_holders_count()
# holders_update('0x9Dc13931B51f974D8d7D85Af272B4c80E4B0E809', 1, 0)
if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    # logging.info("Main    : before creating thread")
    ##
    #   Create Threads
    ##
    th_scan_bsc = threading.Thread(target=thread_scan_bsc, args=())
    # th_scan_eth = threading.Thread(target=thread_scan_eth, args=())
    # th_twitter = threading.Thread(target=thread_twitter, args=())

    th_telegram = threading.Thread(target=thread_telegram, args=())


    ##
    #   Start Threads
    ##
    # th_scan_bsc.start()
    # th_twitter.start()

    # th_telegram.start()


## 0 == ETH, 1 == BSC
####################
#       Loop       #
####################
# while True:
#     try:
#         ############################
#         #       Transactions       #
#         ############################
#         # scan_run_eth()
#         scan_run_bsc()


#         #################################
#         #       Gather Statistics       #
#         #################################

#         # Check twitter status of official account
#         # pawth_twitter_poll_user()

#         # Check top holder stats + make tweet
#         # pawth_stats_holders()

#         #More stats
#         # (statsBuyWallLength, statsBiggestBuy) = botGetStats()
#         # print(" >> BUY WALL LENGTH = " + str(statsBuyWallLength))
#         # print(" >> BIGGEST BUY = " + str(statsBiggestBuy))

#         #######################
#         #       Twitter       #
#         #######################
#         ## Holder
#         # tweet_stats_holder_origin()


#         # Testtweet
#         # tweet_pawth_test()


#         print(" >>> Sleep for 1 min ")

#         time.sleep(60)



#     except Exception as e:
#         print(e)
#         time.sleep(10)