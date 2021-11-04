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


with daemon.DaemonContext():
    bot = telebot.TeleBot(BOT_TOKEN)


    @bot.message_handler(commands=['Help', 'help'])
    def help(message):
        bot.send_message(message.chat.id, '/Price "ticker" to get the Price from the last 10 minutes. ' + "\n" + "\n" +
                         '/Volume "ticker" to get the Volume from the last 10 minutes.' + "\n" + "\n" +
                         '/Ticker and the name of the company to get the ticker symbol. sample: united_internet' + "\n" + "\n" +
                         '/Get "ticker" to see the current Price from yahoo finance. ' + "\n" + "\n" +
                         '/Rsi "ticker" for RSI Indicator.' + "\n" + "\n" +
                         '/Macd "ticker" for MACD indicator.' + "\n" + "\n" +
                         '/Sma "ticker" for SMA 20/50/100/200 Indicator.' + "\n" + "\n" +
                         '/Indices - shows a list of Indices' + "\n" + "\n" +
                         '/Dax - shows a list of all DAX stocks' + "\n" + "\n" +
                         '/Tecdax - shows a list of all TECDAX stocks' + "\n" + "\n" +
                         '/Sdax - shows a list of all SDAX stocks' + "\n" + "\n" +
                         '/Mdax - shows a list of all MDAX stocks' + "\n" + "\n" +
                         '/Dowjones - shows a list of all Dow Jones stocks' + "\n" + "\n" +
                         '/Nasdaq100 - shows a list of all NASDAQ 100 stocks' + "\n" + "\n")

    @bot.message_handler(commands=['Hello', 'hello'])
    def hello(message):
        bot.send_message(message.chat.id, "Hello")


    @bot.message_handler(commands=['Indices', 'indices'])
    def send_indices(message):
        # request = message.text.split()[1].lower()
        reply_text = "\n".join(' =  '.join((key, val)) for (key, val) in ticker.items())
        bot.reply_to(message, reply_text)


    @bot.message_handler(commands=['Dax', 'dax'])
    def send_dax(message):
        # request = message.text.split()[1].lower()
        reply_text = "\n".join(' =  '.join((key, val)) for (key, val) in dax.items())
        bot.reply_to(message, reply_text)


    @bot.message_handler(commands=['Mdax', 'mdax'])
    def send_mdax(message):
        # request = message.text.split()[1].lower()
        reply_text = "\n".join(' =  '.join((key, val)) for (key, val) in mdax.items())
        bot.reply_to(message, reply_text)


    @bot.message_handler(commands=['Tecdax', 'tecdax'])
    def send_tecdax(message):
        # request = message.text.split()[1].lower()
        reply_text = "\n".join(' =  '.join((key, val)) for (key, val) in tecdax.items())
        bot.reply_to(message, reply_text)


    @bot.message_handler(commands=['Sdax', 'sdax'])
    def send_sdax(message):
        # request = message.text.split()[1].lower()
        reply_text = "\n".join(' =  '.join((key, val)) for (key, val) in sdax.items())
        bot.reply_to(message, reply_text)


    @bot.message_handler(commands=['Dowjones', 'dowjones'])
    def send_dowjones(message):
        # request = message.text.split()[1].lower()
        reply_text = "\n".join(' =  '.join((key, val)) for (key, val) in dowjones.items())
        bot.reply_to(message, reply_text)


    @bot.message_handler(commands=['Nasdaq100', 'nasdaq100'])
    def send_nasdaq100(message):
        # request = message.text.split()[1].lower()
        reply_text = "\n".join(' =  '.join((key, val)) for (key, val) in nasdaq100.items())
        bot.reply_to(message, reply_text)

    @bot.message_handler(commands=['Volume', 'volume'])
    def send_volume(message):
        request = message.text.split()[1]
        data = yf.download(tickers=request, period='10m', interval='1m')
        if data.size > 0:
            data = data.reset_index()
            data["format_date"] = data['Datetime'].dt.strftime('%d/%m %H:%M %p')
            data.set_index('format_date', inplace=True)
            data.to_string()
            bot.reply_to(message, data['Volume'].to_string)
        else:
            bot.reply_to(message, "No Data!!")

    @bot.message_handler(commands=['Price', 'price'])
    def send_price(message):
        request = message.text.split()[1]
        data = yf.download(tickers=request, period='10m', interval='1m')
        if data.size > 0:
            data = data.reset_index()
            data["format_date"] = data['Datetime'].dt.strftime('%d/%m %H:%M %p')
            data.set_index('format_date', inplace=True)
            data.to_string()
            bot.reply_to(message, data['Close'].to_string(header=False))
        else:
            bot.reply_to(message, "No Data!!")


    @bot.message_handler(commands=['Ticker', 'ticker'])
    def custom_reply(message):
        request = message.text.split()[1].lower()
        reply_text = CUSTOM_REPLIES.get(request)
        dax_text = dax.get(request)
        tecdax_text = tecdax.get(request)
        sdax_text = sdax.get(request)
        mdax_text = mdax.get(request)
        dowjones_text = dowjones.get(request)
        nasdaq100_text = nasdaq100.get(request)
        if reply_text:
            bot.reply_to(message, reply_text)
        elif dax_text:
            bot.reply_to(message, dax_text)
        elif tecdax_text:
            bot.reply_to(message, tecdax_text)
        elif sdax_text:
            bot.reply_to(message, sdax_text)
        elif mdax_text:
            bot.reply_to(message, mdax_text)
        elif dowjones_text:
            bot.reply_to(message, dowjones_text)
        elif nasdaq100_text:
            bot.reply_to(message, nasdaq100_text)
        else:
            bot.reply_to(message, "No Data!!")

    @bot.message_handler(commands=['Get', 'get'])
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

    @bot.message_handler(commands=['Rsi', 'rsi'])
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

    @bot.message_handler(commands=['Macd', 'macd'])
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

    @bot.message_handler(commands=['Sma', 'sma'])
    def send_sma(message):
        request = message.text.split()[1]
        ticker = request
        start = dt.datetime.now() - dt.timedelta(days=1095)
        end = dt.datetime.now()
        df = web.DataReader(ticker, 'yahoo', start, end)

        def SMA(df, period=30, column='Close'):
            return df[column].rolling(window=period).mean()

        df['SMA20'] = SMA(df, 20)
        df['SMA50'] = SMA(df, 50)
        df['SMA100'] = SMA(df, 100)
        df['SMA200'] = SMA(df, 200)

        plt.figure(figsize=(12, 8))
        ax1 = plt.subplot()
        ax1.set_facecolor('black')
        ax1.set_title(f"Close Price {ticker}", color='black')
        ax1.plot(df['Close'], alpha=0.5, label='Close', color='#CDC0B0')
        ax1.plot(df['SMA20'], alpha=0.5, label='SMA20', color='#97FFFF')
        ax1.plot(df['SMA50'], alpha=0.5, label='SMA50', color='#32cd32')
        ax1.plot(df['SMA100'], alpha=0.5, label='SMA100', color='#0000CD')
        ax1.plot(df['SMA200'], alpha=0.5, label='SMA200', color='#FF0000')
        ax1.legend(facecolor='gray')
        ax1.grid(True)
        ax1.set_axisbelow(True)
        ax1.tick_params(axis='x')
        ax1.tick_params(axis='y')
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        im = Image.open(buf)
        plt.draw()
        bot.send_photo(message.chat.id, im)


    bot.infinity_polling()
