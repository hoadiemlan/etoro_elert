import http.client, urllib, base64, re
import requests
import time
from myform import *

alert_list = []

def history(a):
    body = a[2:-4]
    closeprice = []

    for key in body:
        if "Close" in key:
            c = key.split(':')
            close = float(re.findall('\d+\.\d+', c[1])[0])
            closeprice.append(close)
    return closeprice


stop = 0
prev_price = 0
stick = 0

def check(prev_price):
    duration = "OneMinute"
    item_id = 18
    # create link
    if duration == "OneMinute":
        link = "/candles/desc.json/OneMinute/10/" + str(item_id)
    elif duration == "FiveMinutes":
        link = "/candles/desc.json/FiveMinutes/10/" + str(item_id)
    elif duration == "TenMinutes":
        link = "/candles/desc.json/TenMinutes/10/" + str(item_id)
    elif duration == "OneHour":
        link = "/candles/desc.json/OneHour/10/" + str(item_id)
    else:
        link = "/candles/desc.json/FiveMinutes/10/" + str(item_id)

    # get data from database
    conn = http.client.HTTPConnection('candle.etoro.com')
    conn.request("GET", link)
    response = conn.getresponse()
    data = str(response.read())
    a = data.split(',')
    closeprice = history(a)
    closeprice = closeprice[::-1]
    conn.close()

    last_price = closeprice[-1]
    del_price = abs(last_price - prev_price)
    if ( del_price >= 1):
        messg.showinfo("", str(prev_price)+" "+str(last_price)+" "+str(round(del_price, 2)))
        prev_price = round(last_price, 0)
        # prev_price = round(last_price-last_price%0.5, 2)
    return prev_price
    #     n_alert=1
    #     if (prev_price in alert_list):
    #         n_alert = 10
    #     for i in range(n_alert):
    #         # telegram_bot_sendtext("Price accoss " + str(prev_price) +"  Delta = " +str(del_price))
    #         messg.showinfo("", str(prev_price) + " " + str(del_price))
    #         time.sleep(1)
    # stick = stick+1
    # if stick == 10:
    #     stick = 0
    #     # telegram_bot_sendtext("Price accoss " + str(prev_price) +"  Delta = " +str(del_price))
    #     messg.showinfo("", str(prev_price) + " " + str(del_price))
# prev_price = 0
# for i in range(3):
#     prev_price = check(prev_price)
prev_price = 0
while (1):
    try:
        prev_price = check(prev_price)
    except:
        time.sleep(5)
