
#########################
#       Imports         #
#########################
import tweepy
import threading
import time
from time import sleep
import json
import os.path
from icons import *  
if(os.path.exists("authentication_keys.py")):
    from authentication_keys import *  
    run_mode = 1
else:
    from authentication_keys_template import *
    run_mode = 2


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

def pawth_poll_user():
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
        pawth_poll_user()
        time.sleep(10)

    except Exception as e:
        print(e)
        time.sleep(10)