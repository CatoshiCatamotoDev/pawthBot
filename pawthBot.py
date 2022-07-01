#########################
#       Imports         #
#########################
import threading
import time
from time import sleep
import os.path
from stats.holders import *
from stats.txs import *

from utils.utils import *
from etherscan_requests import *
from ethplorer_requests import *
from thegraph_requests import *

from scan_transactions import *

from icons import *  


userName = ""
userLocation = ""
userDescription = ""
userStatus = ""
userStatusId = ""

####################
#       Loop       #
####################
while True:
    try:
        ############################
        #       Transactions       #
        ############################
        scan_run_eth()
        scan_run_bsc()


        #################################
        #       Gather Statistics       #
        #################################

        # Check twitter status of official account
        # pawth_twitter_poll_user()

        # Check top holder stats + make tweet
        # pawth_stats_holders()

        #More stats
        # (statsBuyWallLength, statsBiggestBuy) = botGetStats()
        # print(" >> BUY WALL LENGTH = " + str(statsBuyWallLength))
        # print(" >> BIGGEST BUY = " + str(statsBiggestBuy))

        #######################
        #       Twitter       #
        #######################
        ## Holder
        # tweet_stats_holder_origin()


        # Testtweet
        # tweet_pawth_test()


        print(" >>> Done ")

        time.sleep(10)



    except Exception as e:
        print(e)
        time.sleep(10)