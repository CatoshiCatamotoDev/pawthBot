import pandas as pd
import plotly.graph_objects as go

from PIL import Image
import json
from datetime import datetime

pyLogo = Image.open("img_pawth_eth.png")
pyLogo2 = Image.open("img_usd.png")
pyLogo3 = Image.open("img_pawth.png")

#####################
#       BSC         #
#####################
# prices_json = json.load(open("./prices_bnb.json", "rt"))

# datesArr = []
# pricesArr = []

# swaps = prices_json.items()
    
# fig = go.Figure()
# for swap, prices in swaps:
#     # print("ii" + str(len(test[swap])))
#     datesArr = []
#     pricesArr = []

#     for i in range(0, len(prices_json[swap])):
#         datesArr.append(prices_json[swap][i]["date"])
#         pricesArr.append(prices_json[swap][i]["price"])

#     dates = pd.DataFrame({'Date': datesArr})
#     print(dates)
#     dates.set_index('Date', inplace = True)

#     fig.add_trace(
#         go.Scatter(name=swap, x=dates.index, y=pricesArr,  mode="lines")
#     )

#####################
#       ETH         #
#####################
prices_json = json.load(open("./prices_radio_usdc.json", "rt"))
prices_eth = json.load(open("./prices_usdt.json", "rt"))
print(prices_eth)
datesArr = []
pricesArr = []

swaps = prices_json.items()
    
fig = go.Figure()
for swap, prices in swaps:
    # print("ii" + str(len(test[swap])))
    datesArr = []
    pricesArr = []

    print("DATE FOUND00!!!!")
    print(len(prices_eth["UNISWAP_TETH"]))

    price_eth = 1


    for i in range(0, len(prices_json[swap])):
        date_orig = prices_json[swap][i]["date"]

        # # date_time_str = '18/09/19 01:55:19'
        # print(date_orig)
        # date_time_str = '2022-02-28T18:29:51'
        date_time_obj = datetime.strptime(date_orig, '%Y-%m-%dT%H:%M:%S')
        # print(date_time_obj)
        for k in range(0, len(prices_eth["UNISWAP_TETH"])):
            date_orig_usdt = prices_eth["UNISWAP_TETH"][k]["date"]
            date_time_obj_usdt = datetime.strptime(date_orig_usdt, '%Y-%m-%dT%H:%M:%S')
            # print(date_time_obj_usdt.date)
            if(date_time_obj.day == date_time_obj_usdt.day and date_time_obj.month == date_time_obj_usdt.month and date_time_obj.year == date_time_obj_usdt.year):
                # print("P1 = " + str(prices_json[swap][i]["price"]))
                # print("P2 = " + str(prices_eth["UNISWAP_TETH"][k]["price"]))
                price_eth = int(prices_eth["UNISWAP_TETH"][k]["price"])
                # print(date_time_obj.day)
                # print(date_time_obj_usdt.day)
                break 
            # print(date_time_obj)

        # print(date_time_obj.day) 
        datesArr.append(prices_json[swap][i]["date"])

        # Price in USDT!
        # pricesArr.append(price_eth/prices_json[swap][i]["price"])#/price_eth)

        pricesArr.append(1/prices_json[swap][i]["price"])#/price_eth)

    dates = pd.DataFrame({'Date': datesArr})
    # print(dates)
    dates.set_index('Date', inplace = True)

    fig.add_trace(
        go.Scatter(name=swap+"🚀", x=dates.index, y=pricesArr,  mode="lines")
    )




# fig.add_layout_image(
#     dict(
#         source=pyLogo, 
#         # xref="x", yref="y", # reference to axis not to paper
#         x=0.1, y=0.8,         # position
#         sizex=0.2, sizey=0.2,   # size
#     )
# )
fig.add_layout_image(
    dict(
        source=pyLogo2, 
        # xref="x", yref="y", # reference to axis not to paper
        x=0.4, y=0.8,         # position
        sizex=0.2, sizey=0.2,   # size
    )
)
fig.add_layout_image(
    dict(
        source=pyLogo3, 
        # xref="x", yref="y", # reference to axis not to paper
        x=0.2, y=0.8,         # position
        sizex=0.2, sizey=0.2,   # size
    )
)

fig.show()

fig.update_layout(template="plotly_white")
fig.write_image("price_pawth_per_eth.png")