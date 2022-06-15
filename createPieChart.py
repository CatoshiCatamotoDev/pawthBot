import pandas as pd 
import matplotlib.pyplot as plt
# Import the json

def createPyChart():

    df = pd.read_json("./holders.json")

    # Specify accounts that are not normal holders

    dead = '0x000000000000000000000000000000000000dead'

    uniswap = '0x800a45f2b861229d59e952aef57b22e84ff949a1'
    devWallet = "0x16b1db77b60c8d8b6ecea0fa4e0481e9f53c9ba1"
    bigOne = "0xd4dcd2459bb78d7a645aa7e196857d421b10d93f"
    bsc = "0xdfed31e640b7280f76f046a97179e5e369d209b5"

    list_of_accounts_to_exclude = [dead,devWallet,uniswap,bigOne,bsc]

    # Create lists of all of these addresses, balances, and shares to create your pie chart

    list_of_addresses = []
    list_of_balances = []
    list_of_shares = []
    i = 0


    for holder in df['holders']:
        if holder['address'] == dead:
            list_of_addresses.append("Burned")
        if holder['address'] == uniswap:
            list_of_addresses.append("Uniswap")
        if holder['address'] == bigOne:
            list_of_addresses.append("BigOne")
        if holder['address'] == bsc:
            list_of_addresses.append("Bsc Bridge")   
        if holder['address'] == devWallet:
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
    plt.show()

createPyChart()