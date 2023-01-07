import requests
import os
from datetime import datetime
from datetime import timedelta
import html
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
import os

account_sid = "ur_account_sid"
auth_token = "your_auth_token"
twilio_phone_number = "the_phone_number_from_twilio"
to_telephone_number = "phone_number_you_wanna_send_message"



STOCK = "TSLA"
COMPANY_NAME = "tesla"
API_KEY = "M4T3R72HJY6D6BBN"
INTERVAL = "60min"
API_KEY2 = "deb3ef0a994048d592d5eda68dbf7601"


today = datetime.today()
yesterday = (today - timedelta(days = 1)).strftime("%Y-%m-%d")
the_day_before_yesterday = (today - timedelta(days = 2)).strftime("%Y-%m-%d")

response = requests.get(url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={STOCK}&interval={INTERVAL}&apikey={API_KEY}')
data = response.json()

yesterday_stock_price = float(data[f"Time Series ({INTERVAL})"][f"{yesterday} 16:00:00"]["4. close"])
the_day_before_yesterday_price = float(data[f"Time Series ({INTERVAL})"][f"{the_day_before_yesterday} 16:00:00"]["4. close"])
last_stock_price = float(list(data[f"Time Series ({INTERVAL})"].items())[0][1]["4. close"])

if (last_stock_price < (yesterday_stock_price - yesterday_stock_price * 0.1)) or \
   (last_stock_price > (yesterday_stock_price + yesterday_stock_price * 0.1)) or \
   (last_stock_price < (the_day_before_yesterday_price - the_day_before_yesterday_price * 0.1)) or \
   (last_stock_price > (the_day_before_yesterday_price + the_day_before_yesterday_price * 0.1)) :


    response = requests.get(url=f"https://newsapi.org/v2/everything?q={COMPANY_NAME}&from={(today - timedelta(days=10)).strftime('%Y-%m-%d')}&sortBy=publishedAt&apiKey={API_KEY2}")
    data = response.json()
    contents = list()
    for i in range(3):
        contents.append((html.unescape(data["articles"][i]["title"]),html.unescape(data["articles"][i]["content"]) ))

    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {"https": os.environ["http_proxy"]}

    client = Client(account_sid, auth_token, http_client=proxy_client)
    for headline_,message_ in contents:
        if last_stock_price > yesterday_stock_price or last_stock_price > the_day_before_yesterday_price:
            message = client.messages.create(body=f"{STOCK}: 🔺10%\nHeadline: {headline_}\nBrief: {message_}"
                                            , from_=twilio_phone_number
                                            , to=to_telephone_number)
            print(message.status)

        elif last_stock_price < yesterday_stock_price or last_stock_price < the_day_before_yesterday_price:
            message = client.messages.create(body=f"{STOCK}: 🔻10%\nHeadline: {headline_}\nBrief: {message_}"
                                             , from_=twilio_phone_number
                                             , to=to_telephone_number)

            print(message.status)


