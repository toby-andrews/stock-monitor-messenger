import requests
import datetime
from twilio.rest import Client
import os

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")

account_sid = TWILIO_ACCOUNT_SID
auth_token = TWILIO_AUTH_TOKEN

api_stocks = "5R5RZJPUZKCNEF34"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 2% between yesterday and the day before yesterday then print("Get News").
parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": api_stocks,
}

# Get dates
date = datetime.date.today()
yesterday = str(date - datetime.timedelta(days=1))
two_days_ago = str(date - datetime.timedelta(days=2))

# Pull data
response = requests.get(url='https://www.alphavantage.co/query', params=parameters)
response.raise_for_status()
data_package = response.json()
# print(data_package)
stock_data = data_package["Time Series (Daily)"]
yesterday_data_open = float(stock_data[yesterday]["1. open"])
# print(yesterday_data_open)
two_day_close = float(stock_data[two_days_ago]["4. close"])
# print(two_day_close)


## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")

parameters_2 = {
    "apikey": "48939019a91741f988b6f698b95bede3",
    "q": "tesla",
}

response2 = requests.get(url="https://newsapi.org/v2/everything", params=parameters_2)
response.raise_for_status()

# This is the first way to access the data. I would make the num a variable and add 1 in a for loop
# news_article_title = response2.json()["articles"][0]["title"]
# news_article_brief = response2.json()["articles"][0]["description"]
# print(news_article_title)
# print(news_article_brief)

# This is the more refined way to do with slices.
test = response2.json()["articles"]
test_slice = test[:3]
articles = []
for article in test_slice:
    articles.append(article["title"])
    articles.append(article["description"])


## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 

def send_message():
    x = 0
    while x < 6:
        client = Client(account_sid, auth_token)

        headline = f"Headline: {articles[x]}"
        x += 1
        brief = f"Brief: {articles[x]}"
        x += 1

        message = client.messages \
            .create(
            body=f"{STOCK} {difference}%\n{headline}\n{brief}",
            from_='+19036023157',
            to='+12053928453'
        )

        print(message.status)

# Find % difference and call function to send message
difference = (((yesterday_data_open - two_day_close) / yesterday_data_open) * 100)
if difference > 2 or difference < -2:
    send_message()
