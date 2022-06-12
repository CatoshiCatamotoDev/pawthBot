
#########################
#       Imports         #
#########################
import tweepy
import threading
import time
from time import sleep
import os.path

from etherscan_requests import *
from ethplorer_requests import *

from icons import *  
if(os.path.exists("authentication_keys.py")):
    from authentication_keys import *  
    run_mode = 1
else:
    from authentication_keys_template import *
    run_mode = 2


# Pawthereum Token Address
TOKEN_ADDRESS = "0xAEcc217a749c2405b5ebC9857a16d58Bdc1c367F"


###########################
#    Global Variables     #
###########################
global userObj


#####################
#    Startup        #
#####################
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
def pawthBot_tweet(changeType, old, new):
    if(changeType == 1):
        msg = "Pawth - Username changed: \n - "+iconCrossMark+"Old: "+old+"\n - "+iconEyes+"New: " + new
        print(">>> New status update:")
        print(msg)
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

def util_commify(value):
    # Round value (remove value after decimal point)
    # Add comma's to make more readable
    return ("{:,}".format(round(value)))

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
    msg = iconFire + "$PAWTH Thresholds: " + iconFire + "\n"
    msg += "\n > top 3: " + str(util_commify(holder3['balance']/1e9)) + " (" + str(holder3['share']) +"%)"
    msg += "\n > top 10: " + str(util_commify(holder10['balance']/1e9)) + " (" + str(holder10['share']) +"%)"
    msg += "\n > top 50: " + str(util_commify(holder50['balance']/1e9)) + " (" + str(holder50['share']) +"%)"
    msg += "\n > top 100: " + str(util_commify(holder100['balance']/1e9)) + " (" + str(holder100['share']) +"%)"

    msg += "\n\nNote: this excludes the dead wallet which holds 14.2%"
    print(msg)
    apiObj.update_status(msg)


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
        # Check twitter status of official account
        # pawth_twitter_poll_user()

        # Check top holder stats + make tweet
        pawth_stats_holders()

        time.sleep(10)

    except Exception as e:
        print(e)
        time.sleep(10)