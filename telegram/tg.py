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
from icons import *  

import telebot
from telebot import types

catIcon1="😻"
catIcon2="🙀"
catIcon3="🐈‍⬛"
catIcon4="😸"
greenHeartIcon="💚"
redHeartIcon="❤️"

sys.path.append('..')
TELEGRAM_API_KEY = "5574053127:AAEIv2W-kM3Xl74pioYDRQ1zteL-9zLKp2U"
VERSION_STR="0.01"

bot = telebot.TeleBot(TELEGRAM_API_KEY)

MSG_HEADER_ABOUT = "* ABOUT * \n"
MSG_HEADER_HOLDERS = "* HOLDERS DISTRIBUTION * \n"
MSG_HEADER_PRICES = "* PRICES INFORMATION * \n"
MSG_HEADER_BUYSELL = "* LAST 10 TRANSACTIONS * \n"
MSG_HEADER_RANKING = iconRocket + "* RANKING * " + iconRocket + "\n"
MSG_HEADER_LASTUPDATE = iconTime + "* Last Updated: * " + iconTime + "\n"
MSG_HEADER_WHALES = iconWhale + " *Whale Dominance: *" + iconWhale + "\n"
MSG_HEADER_THRESHOLDS = iconCrossedSwords + " $PAWTH Thresholds: " + iconCrossedSwords + "\n"

def createMessageHolders():

    markup = MSG_HEADER_HOLDERS
    
    markup += " > The image shows you the holder distribution. \n" 
    markup += "\n"

    return markup

def createMessagePrices():

    markup = MSG_HEADER_PRICES
    
    markup += " > The image shows you the amount of Pawth you can get per ETH or BNB over time \n" 
    markup += "\n"

    return markup


def createMessageBuySell():

    markup = MSG_HEADER_BUYSELL
    transactions_eth = json.load(open("transactions-state-eth.json", "rt"))
    eth_last_update_formatted = ctime(transactions_eth["last_scanned_time"])

    msg_test = "``` === ETHEREUM ===  (last update: " + eth_last_update_formatted + ")```\n"

    # bsc_last_update_formatted = ctime(bsc_update["last_scanned_time"])

    # print(eth_last_update_formatted)


    eth_last_transaction = transactions_eth["blocks"]
    eth_list = list(eth_last_transaction)

    for i in range(-11,-1):
        eth_last_t = eth_last_transaction[eth_list[i]]
        print(eth_last_t)

        pairs2 = eth_last_t.items()
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
                msg_test += transfer_investigate(transfer, tx_id, 0)


    # print(eth_last_t)
    # bsc_last_update_formatted = ctime(bsc_update["last_scanned_time"])

    ###
    # BSC
    ###
    transactions_bsc = json.load(open("transactions-state-bsc.json", "rt"))

    bsc_last_update_formatted = ctime(transactions_bsc["last_scanned_time"])
    bsc_last_transaction = transactions_bsc["blocks"]

    bsc_list = list(bsc_last_transaction)
    msg_test += "```\n\n === BINANCE SMART CHAIN === (last update: " + bsc_last_update_formatted + ")```\n"

    for i in range(-11,-1):
        bsc_last_t = bsc_last_transaction[bsc_list[i]]
        # print(bsc_last_t)

        pairs2 = bsc_last_t.items()
        for tx_id, value2 in pairs2:
            # print(tx_id)
            # print(value2)

            pairs3 = value2.items()
            # print("LEN = " + str(len(value2)))
            # if(len(value2) > 20):
                # print(key2)
                # print(value2)
            for log_id, transfer in pairs3:
                # print(">>>> KAKAKAKAKAKA")
                # print(transfer)

                msg_test += transfer_investigate(transfer, tx_id, 1)

    markup += msg_test 
    # markup += " > BSC:  " + bsc_last_update_formatted + "\n" 

    markup += "\n"

    return markup



def createMessageWhales():

    print(" >>>>  Whales!")

    markup = MSG_HEADER_WHALES
    msg = str(stats_holders_whale_dominance())
    markup += msg

    return markup    


def createMessageThresholds():

    print(" >>>>  Thresholds!")

    markup = MSG_HEADER_THRESHOLDS
    
    msg = str(stats_holders_thresholds())
    markup += msg

    return markup    


def createMessageAbout():

    print(" >>>>  ABOUT!")

    markup = MSG_HEADER_ABOUT
    
    markup += " > This Bot is made with " + redHeartIcon + " by the [Pawthereum Community](https://www.pawthereum.com) \n" 
    markup += " > VERSION: " + VERSION_STR + "\n"
    markup += "\n"

    return markup    

def createMessageRanking(ranking, value):
    print(" >>>>  Ranking!")

    markup = MSG_HEADER_RANKING
    
    markup += " > Ranking:  " + str(ranking) + "\n" 
    markup += " > Value:  " + str(util_commify(value/1e9)) + " PAWTH\n" 
    markup += "\n"

    return markup    

import os

def createMessageLastUpdate():
    print(" >>>>  LastUpdate!")

    markup = MSG_HEADER_LASTUPDATE
    #to get the current working directory
    directory = os.getcwd()

    print(directory)
    eth_update = json.load(open("transactions-state-eth.json", "rt"))
    bsc_update = json.load(open("transactions-state-bsc.json", "rt"))

    eth_last_update_formatted = ctime(eth_update["last_scanned_time"])
    bsc_last_update_formatted = ctime(bsc_update["last_scanned_time"])

    print(eth_last_update_formatted)
    markup += " > ETH:  " + eth_last_update_formatted + "\n" 
    markup += " > BSC:  " + bsc_last_update_formatted + "\n" 

    markup += "\n"

    return markup    


@bot.message_handler(commands=['lastupdate'])
def handle_command_adminwindow(message):
    chatId = message.chat.id
    print("CHATID = " + str(message.chat.id))
    (markup) = createMessageLastUpdate()
    bot.send_message(chat_id=chatId,
                text=markup, 
                parse_mode= 'Markdown', disable_web_page_preview=True)

@bot.message_handler(commands=['about'])
def handle_command_adminwindow(message):
    chatId = message.chat.id
    print("CHATID = " + str(message.chat.id))
    (markup) = createMessageAbout()
    bot.send_message(chat_id=chatId,
                text=markup, 
                parse_mode= 'Markdown', disable_web_page_preview=True)


@bot.message_handler(commands=['ranking'])
def handle_command_adminwindow(message):
    
    chatId = message.chat.id

    # Check if input is ok
    # TODO: needs better check (e.g. check if second parameter is valid address)
    if len(message.text.split()) == 2:
        print(message.text)
        command, addr = message.text.split()
        print(addr)

        print("Ranking of addr=" + addr)
        
        print("CHATID = " + str(message.chat.id))
        ranking, value = stats_holders_ranking(addr)

        print("RANKING = " + str(ranking))
        (markup) = createMessageRanking(ranking, value)


    else:
        markup = " Please provide valid address as parameter.\n"
        markup += " e.g. /ranking 0x1234"
        print("EXCEPTION ")

    
    bot.send_message(chat_id=chatId,
                text=markup, 
                parse_mode= 'Markdown', disable_web_page_preview=True)

    test = stats_my_transactions(addr)
    markup = test
    bot.send_message(chat_id=chatId,
                text=markup, 
                parse_mode= 'Markdown', disable_web_page_preview=True)

@bot.message_handler(commands=['holders'])
def handle_command_adminwindow(message):
    print("HOLDERS!!")
    # stats_holders_origin()


    ## IMGPLOT not thread save.. cannot pproduce the image in this thread...
    # img = stats_holders_originc()
    # img.show()
    # plt.savefig("test.png")

    chatId = message.chat.id
    print("CHATID = " + str(message.chat.id))

    (markup) = createMessageHolders()
    bot.send_message(chat_id=chatId,
                text=markup, 
                parse_mode= 'Markdown', disable_web_page_preview=True)

    img = open('holder_origin_pie_chart.png', 'rb')
    bot.send_photo(chatId, img)
    img.close()


@bot.message_handler(commands=['prices'])
def handle_command_adminwindow(message):

    chatId = message.chat.id
    print("CHATID = " + str(message.chat.id))

    (markup) = createMessagePrices()
    bot.send_message(chat_id=chatId,
                text=markup, 
                parse_mode= 'Markdown', disable_web_page_preview=True)

    img = open('price_pawth_per_bnb.png', 'rb')
    bot.send_photo(chatId, img)
    img = open('price_pawth_per_eth.png', 'rb')
    bot.send_photo(chatId, img)
    img.close()


@bot.message_handler(commands=['lasttransactions'])
def handle_command_adminwindow(message):
    print("BUYS&SELLS!!")
    # stats_holders_origin()


    ## IMGPLOT not thread save.. cannot pproduce the image in this thread...
    # img = stats_holders_originc()
    # img.show()
    # plt.savefig("test.png")

    chatId = message.chat.id
    print("CHATID = " + str(message.chat.id))

    (markup) = createMessageBuySell()
    bot.send_message(chat_id=chatId,
                text=markup, 
                parse_mode= 'Markdown', disable_web_page_preview=True)




@bot.message_handler(commands=['whales'])
def handle_command_adminwindow(message):

    chatId = message.chat.id

    (markup) = createMessageWhales()
    bot.send_message(chat_id=chatId,
                text=markup, 
                parse_mode= 'Markdown', disable_web_page_preview=True)

@bot.message_handler(commands=['thresholds'])
def handle_command_adminwindow(message):

    chatId = message.chat.id

    (markup) = createMessageThresholds()
    bot.send_message(chat_id=chatId,
                text=markup, 
                parse_mode= 'Markdown', disable_web_page_preview=True)



def thread_telegram():
    while(1):
        try: 
            print("TELEGRAM")
            bot.polling(none_stop=True, interval=2, timeout=2)
            print("TEST!!")
            time.sleep(2)

        except Exception as e:
            print(">> EXCEPTION")
            print(e)
            time.sleep(1)            


        #Polling Thread to intercept commands
# def threadCommands():
#     while True:

#         else:
#             bot.stop_polling()
#             print("Bot polling loop finished")
#             time.sleep(10)