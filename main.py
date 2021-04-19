import http.client, urllib, base64, re
import requests
import time


alert_list = [1767, 1767.5, 1765, 1763.5, 1760]


def history(a):
    body = a[2:-4]
    closeprice = []

    for key in body:
        if "Close" in key:
            c = key.split(':')
            close = float(re.findall('\d+\.\d+', c[1])[0])
            closeprice.append(close)
    return closeprice


def telegram_bot_sendtext(bot_message):
    bot_token = '1495511574:AAEXKD5LND4FpYFJCY-z6vG0h15kPGT1TOc'
    bot_chatID = '1080795442'  # Duong
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()


telegram_bot_sendtext("Start alert")
stop = 0
prev_price = 0
while (1):
    try:
        while (stop != 1):
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
            conn = http.client.HTTPSConnection('candle.etoro.com')
            conn.request("GET", link)
            response = conn.getresponse()
            data = str(response.read())
            a = data.split(',')
            closeprice = history(a)
            closeprice = closeprice[::-1]
            conn.close()

            last_price = closeprice[-1]
            del_price = abs(last_price - prev_price)
            if ( del_price > 0.5):
                prev_price = round(last_price-last_price%0.5, 2)
                n_alert=1
                if (prev_price in alert_list):
                    n_alert = 10
                for i in range(n_alert):
                    telegram_bot_sendtext("Price accoss " + str(prev_price) +"  Delta = " +str(del_price))
                    time.sleep(1)
            # for iprice in alert_list:
            #     if (prev_price > iprice > last_price or prev_price < iprice < last_price):
            #         telegram_bot_sendtext("Price accoss " + str(iprice))
    except:
        time.sleep(5)

