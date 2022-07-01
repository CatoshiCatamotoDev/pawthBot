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

sys.path.append('..')

import tweepy

#################
#    SETTINGS   #
#################
TWEETS_ENABLED = 0

###########################
#    Global Variables     #
###########################
global userObj

#####################
#    Startup        #
#####################
def tweets_init():
    if(os.path.exists("authentication_keys.py")):
        from authentication_keys import twitter_acces_secret, twitter_access_token, twitter_consumer_key, twitter_consumer_secret
        run_mode = 1
    else:
        from authentication_keys_template import twitter_acces_secret, twitter_access_token, twitter_consumer_key, twitter_consumer_secret
        run_mode = 2
    print("> Starting Pawthereum Tweetbot:")
    if(run_mode == 1):
        print(" >> Trying to authenticate")
        # Authenticate to Twitter
        auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
        auth.set_access_token(twitter_access_token, twitter_acces_secret)


        #Pawthereum account user
        # Create the API object
        apiObj = tweepy.API(auth)

        try:
            # Verify the credentials
            apiObj.verify_credentials()
            print(" >> Authentication OK")
        except:
            print("Error during authentication")
    elif(run_mode == 2):
        apiObj = 0
        print(" >> No authentication keys are provided. This won't work (yet).")
        exit()

######################
#    Functions       #
######################
def botGetStats():

    # res = run_query(query_token)
    # # pprint(res)
    # resToken = res["data"]["token"]
    # print(resToken)
    # resTokenSymbol = resToken["symbol"]
    # print(resTokenSymbol)

    ###########
    # Tweet 1 - Stats
    ###########

    # statsBuyWallLength = stats_txs_get_buywall_length()
    # print(" BUYWALL=" + str(statsBuyWallLength))


    # statsBiggestBuy = stats_txs_get_biggest_buy()

    # # print(len(resSwaps))
    # msg = iconAbacus + " Statistics (last 100 transactions): " + iconAbacus + "\n"
    # msg +=  " > Biggest Buy Order: " + '{:,}'.format(round(statsBiggestBuy, 3)) + "Ξ \n" 
    # msg += " > Current Buy Streak: " 
    # for j in range(0,statsBuyWallLength):
    #     msg += iconGreenCircle

    # msg += " (" + str(statsBuyWallLength) + ")\n"

    # msg += "\n(1/2)" + iconThread + iconFingerDown

    # print(msg)

    # if(TWEETS_ENABLED == 1):
    #     original_tweet = apiObj.update_status(msg)   

    ###########
    # Tweet 2 - Holder Distribution
    ###########
    # msg = " > Holder Distribution:"

    # msg += "\n(2/2)"

    # print(msg)

    #Generate Image
    # img = stats_holders_distribution()
    # img.show()

    # Upload image
    # media = apiObj.media_upload("saved_pie_chart.png")

    # Post tweet with image
    # if(TWEETS_ENABLED == 1):
    #     reply1_tweet = apiObj.update_status(msg, media_ids=[media.media_id],
    #                                 in_reply_to_status_id=original_tweet.id, 
    #                                 auto_populate_reply_metadata=True)

    ###########
    # Tweet 3 - Holder Origin
    ###########
    img = stats_holders_origin()
    # img.show()


def pawthBot_tweet(changeType, old, new):
    if(changeType == 1):
        msg = "Pawth - Username changed: \n - "+iconCrossMark+"Old: "+old+"\n - "+iconEyes+"New: " + new
        print(">>> New status update:")
        print(msg)
        if(TWEETS_ENABLED == 1):
            apiObj.update_status(msg)

def pawth_twitter_poll_user():
    global userName, userLocation, userDescription, userStatus, userStatusId    

    userObj = apiObj.get_user(screen_name = 'pawthereum')
    # print(userObj)

    #Check username
    if userName != userObj.name:
        # print(" No Diff - " + userName + " -- " + userObj.name)
        # print(" USERNAME DIFF")
        pawthBot_tweet(1, userObj.name, userName)
        userName = userObj.name
    else:
        print(" No Diff - " + userName + " -- " + userObj.name)

    # Check location
    if userLocation != userObj.location:
        userLocation = userObj.location

    # Check description
    if userDescription != userObj.description:
        userDescription = userObj.description
    
    #Check the last tweet:
    if userStatus != userObj.status:
        userStatus = userObj.status
    
    if userStatusId != userObj.id:
        userStatusId = userStatus.id





def tweet_stats_holder_origin():
    holders = stats_holder_origin()

    holders.show()
    msg = iconWhale + " Whale Dominance: " + iconWhale + "\n"

    msg += "\n(1/2)" + iconThread + iconFingerDown

    print(msg)
    # if(TWEETS_ENABLED == 1):
    #     original_tweet = apiObj.update_status(msg)


    # if(TWEETS_ENABLED == 1):
    #     reply1_tweet = apiObj.update_status(msg, 
    #                                 in_reply_to_status_id=original_tweet.id, 
    #                                 auto_populate_reply_metadata=True)






def tweet_pawth_test():
    msg = "Beep Beep Bop " + iconRobot
    print(msg)
    apiObj.update_status(msg)



def pawth_stats_holders():
    holders = get_top_holders()
    
    holder0 = holders[0]
    holder1 = holders[1]
    holder2 = holders[2]
    holder3 = holders[3]
    holder10 = holders[10]
    holder20 = holders[20]
    holder50 = holders[50]
    holder100 = holders[99] #take 99 as we only get 100 values from ethplorer
    # print(str(holder3))


    sumDominance = 0
    msg = iconWhale + " Whale Dominance: " + iconWhale + "\n"

    for i in range(1,3):
        sumDominance += holders[i]['share']        
    msg += " Top 3: " + str(round(sumDominance,2)) + " %\n"

    for i in range(4,10):
        sumDominance += holders[i]['share']        
    msg += " Top 10: " + str(round(sumDominance,2)) + "%\n"

    for i in range(11,50):
        sumDominance += holders[i]['share']        
    msg += " Top 50: " + str(round(sumDominance,2)) + "%\n"

    for i in range(51,99):
        sumDominance += holders[i]['share']        
    msg += " Top 100: " + str(round(sumDominance,2)) + "%\n"

    msg += "\n(1/2)" + iconThread + iconFingerDown

    print(msg)
    if(TWEETS_ENABLED == 1):
        original_tweet = apiObj.update_status(msg)

    msg = iconCrossedSwords + " $PAWTH Thresholds: " + iconCrossedSwords + "\n"
    msg += "\n > top 3: " + str(util_commify(holder3['balance']/1e9)) + " (" + str(holder3['share']) +"%)"
    msg += "\n > top 10: " + str(util_commify(holder10['balance']/1e9)) + " (" + str(holder10['share']) +"%)"
    msg += "\n > top 50: " + str(util_commify(holder50['balance']/1e9)) + " (" + str(holder50['share']) +"%)"
    msg += "\n > top 100: " + str(util_commify(holder100['balance']/1e9)) + " (" + str(holder100['share']) +"%)"

    msg += "\n\nNote: the dead/burn wallet holds 14.2% " + iconFire +"\n"

    msg += "(2/2)"

    print(msg)

    if(TWEETS_ENABLED == 1):
        reply1_tweet = apiObj.update_status(msg, 
                                    in_reply_to_status_id=original_tweet.id, 
                                    auto_populate_reply_metadata=True)


