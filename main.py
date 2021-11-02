import telebot
from settings import *
import yfinance as yf
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
import daemon
from PIL import Image
import matplotlib.pyplot as plt
import datetime as dt
import pandas as pd
import pandas_datareader as web
import io


print("Bot started...")

with daemon.DaemonContext():
    bot = telebot.TeleBot(BOT_TOKEN)


    @bot.message_handler(commands=['Help', 'help'])
    def greet(message):
        bot.reply_to(message, "")


    @bot.message_handler(commands=['Hello', 'hello'])
    def hello(message):
        bot.reply_to(message.chat.id, "Hello")


    def stock_volume(message):
        request = message.text.split()
        if len(request) < 2 or request[0].lower() not in 'volume':
            return False
        else:
            return True


    @bot.message_handler(func=stock_volume)
    def send_volume(message):
        request = message.text.split()[1]
        data = yf.download(tickers=request, period='10m', interval='1m')
        if data.size > 0:
            data = data.reset_index()
            data["format_date"] = data['Datetime'].dt.strftime('%d/%m %H:%M %p')
            data.set_index('format_date', inplace=True)
            print(data.to_string())
            bot.reply_to(message, data['Volume'].to_string)
        else:
            bot.reply_to(message, "No Data!!")


    def stock_price(message):
        request = message.text.split()
        if len(request) < 2 or request[0].lower() not in 'price':
            return False
        else:
            return True


    @bot.message_handler(func=stock_price)
    def send_price(message):
        request = message.text.split()[1]
        data = yf.download(tickers=request, period='10m', interval='1m')
        if data.size > 0:
            data = data.reset_index()
            data["format_date"] = data['Datetime'].dt.strftime('%d/%m %H:%M %p')
            data.set_index('format_date', inplace=True)
            print(data.to_string())
            bot.reply_to(message, data['Close'].to_string(header=False))
        else:
            bot.reply_to(message, "No Data!!")


    def stock_indices(message):
        request = message.text.split()
        if len(request) < 2 or request[0].lower() not in 'indices':
            return False
        else:
            return True


    @bot.message_handler(func=stock_indices)
    def send_indices(message):
        request = message.text.split()[1].lower()
        reply_text = "\n".join(' =  '.join((key, val)) for (key, val) in ticker.items())
        if reply_text:
            bot.reply_to(message, reply_text)
        else:
            bot.reply_to(message, "No Data!!")


    def stock_dax(message):
        request = message.text.split()
        if len(request) < 2 or request[0].lower() not in 'dax':
            return False
        else:
            return True


    @bot.message_handler(func=stock_dax)
    def send_dax(message):
        request = message.text.split()[1].lower()
        reply_text = "\n".join(' =  '.join((key, val)) for (key, val) in dax.items())
        if reply_text:
            bot.reply_to(message, reply_text)
        else:
            bot.reply_to(message, "No Data!!")


    def stock_tecdax(message):
        request = message.text.split()
        if len(request) < 2 or request[0].lower() not in 'tecdax':
            return False
        else:
            return True


    @bot.message_handler(func=stock_tecdax)
    def send_tecdax(message):
        request = message.text.split()[1].lower()
        reply_text = "\n".join(' =  '.join((key, val)) for (key, val) in tecdax.items())
        if reply_text:
            bot.reply_to(message, reply_text)
        else:
            bot.reply_to(message, "No Data!!")


    def stock_dow(message):
        request = message.text.split()
        if len(request) < 2 or request[0].lower() not in 'dow':
            return False
        else:
            return True


    @bot.message_handler(func=stock_dow)
    def send_dow(message):
        request = message.text.split()[1].lower()
        reply_text = "\n".join(' =  '.join((key, val)) for (key, val) in dowjones.items())
        if reply_text:
            bot.reply_to(message, reply_text)
        else:
            bot.reply_to(message, "No Data!!")


    def stock_custom(message):
        request = message.text.split()
        if len(request) < 2 or request[0].lower() not in 'ticker':
            return False
        else:
            return True


    @bot.message_handler(func=stock_custom)
    def custom_reply(message):
        request = message.text.split()[1].lower()
        reply_text = CUSTOM_REPLIES.get(request)
        if reply_text:
            bot.reply_to(message, reply_text)
        else:
            bot.reply_to(message, "No Data!!")


    def stock_get(message):
        request = message.text.split()
        if len(request) < 2 or request[0].lower() not in 'get':
            return False
        else:
            return True


    @bot.message_handler(func=stock_get)
    def send_getData(message):
        ua = UserAgent()
        header = {'User-Agent': str(ua.chrome)}
        request = message.text.split()[1].lower()
        url = f"https://finance.yahoo.com/quote/{request}"
        r = requests.get(url, headers=header)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
        else:
            print("Seite konnte nicht geladen werden.", url)

        stock = (soup.find('h1', {'class': 'D(ib) Fz(18px)'}).text + "\n" +
                 soup.find("div", {"class": "D(ib) Mend(20px)"}).find_all("span")[0].text + "\n" +
                 soup.find("div", {"class": "D(ib) Mend(20px)"}).find_all("span")[1].text + "\n" +
                 soup.find("div", {"class": "C($tertiaryColor) Fz(12px)"}).find_all("span")[0].text + "\n" +
                 soup.find('div', {'class': "C($tertiaryColor) D(b) Fz(12px) Fw(n) Mstart(0)--mobpsm Mt(6px)--mobpsm"}).find_all('span')[0].text)
        bot.send_message(message.chat.id, stock)


    def stock_rsi(message):
        request = message.text.split()
        if len(request) < 2 or request[0].lower() not in 'rsi':
            return False
        else:
            return True


    @bot.message_handler(func=stock_rsi)
    def send_rsi(message):
        request = message.text.split()[1]
        ticker = request
        start = dt.datetime.now() - dt.timedelta(days=365)
        end = dt.datetime.now()

        data = web.DataReader(ticker, 'yahoo', start, end)

        delta = data['Adj Close'].diff(1)
        delta.dropna(inplace=True)

        positive = delta.copy()
        negative = delta.copy()

        positive[positive < 0] = 0
        negative[negative > 0] = 0

        days = 14

        average_gain = positive.rolling(window=days).mean()
        average_loss = abs(negative.rolling(window=days).mean())

        relative_strength = average_gain / average_loss
        RSI = 100.0 - (100.0 / (1.0 + relative_strength))

        combined = pd.DataFrame()
        combined['Adj Close'] = data['Adj Close']
        combined['RSI'] = RSI

        plt.figure(figsize=(12, 8))
        ax1 = plt.subplot(211)
        ax1.plot(combined.index, combined['Adj Close'], color='lightgray')
        ax1.set_title("Adjusted Close Price", color='white')

        ax1.grid(True, color='#555555')
        ax1.set_axisbelow(True)
        ax1.set_facecolor('black')
        ax1.tick_params(axis='x', color='white')
        ax1.tick_params(axis='y', color='white')

        ax2 = plt.subplot(212, sharex=ax1)
        ax2.plot(combined.index, combined['RSI'], color='lightgray')
        ax2.axhline(0, linestyle='--', alpha=0.5, color='red')
        ax2.axhline(10, linestyle='--', alpha=0.5, color='yellow')
        ax2.axhline(20, linestyle='--', alpha=0.5, color='green')
        ax2.axhline(30, linestyle='--', alpha=0.5, color='lightgray')
        ax2.axhline(70, linestyle='--', alpha=0.5, color='lightgray')
        ax2.axhline(80, linestyle='--', alpha=0.5, color='green')
        ax2.axhline(90, linestyle='--', alpha=0.5, color='yellow')
        ax2.axhline(100, linestyle='--', alpha=0.5, color='red')

        ax2.set_title("RSI Value", color='black')
        ax2.grid(False)
        ax2.set_axisbelow(True)
        ax2.set_facecolor('black')
        ax2.tick_params(axis='x', color='white')
        ax2.tick_params(axis='y', color='white')

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        im = Image.open(buf)
        plt.draw()
        bot.send_photo(message.chat.id, im)


    def stock_macd(message):
        request = message.text.split()
        if len(request) < 2 or request[0].lower() not in 'macd':
            return False
        else:
            return True


    @bot.message_handler(func=stock_macd)
    def send_macd(message):
        request = message.text.split()[1]
        ticker = request
        start = dt.datetime.now() - dt.timedelta(days=365)
        end = dt.datetime.now()
        df = web.DataReader(ticker, 'yahoo', start, end)

        ema_26 = df["Adj Close"].ewm(span=26, adjust=False).mean()
        ema_12 = df["Adj Close"].ewm(span=12, adjust=False).mean()
        MACD = ema_12 - ema_26
        signal = MACD.ewm(span=9, adjust=False).mean()

        df["MACD"] = MACD
        df["Signal"] = signal
        plt.figure(figsize=(12, 8))
        ax1 = plt.subplot(211)
        ax1.plot(df['Adj Close'], color='lightgray')
        ax1.set_title(f"Adjusted Close Price {ticker}", color='black')

        ax1.grid(True, color='#555555')
        ax1.set_axisbelow(True)
        ax1.set_facecolor('black')
        ax1.tick_params(axis='x')
        ax1.tick_params(axis='y')

        ax2 = plt.subplot(212, sharex=ax1)
        ax2.plot(df["MACD"], label="MACD")
        ax2.plot(df["Signal"], label="Signal")
        ax2.set_title("MACD", color='black')
        ax2.grid(False)
        ax2.set_axisbelow(True)
        ax2.set_facecolor('black')
        ax2.tick_params(axis='x', color='white')
        ax2.tick_params(axis='y', color='white')
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        im = Image.open(buf)
        plt.draw()
        bot.send_photo(message.chat.id, im)


    bot.infinity_polling()


#main()

# with daemon.DaemonContext():
#    main()
