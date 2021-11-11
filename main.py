import telebot
from settings import *
from description import *
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
    def help(message):
        if message.chat.type == "private" or "group":
            if message.chat.username == None:
                answer = f"Hello {message.from_user.first_name}, you can use the commands below"
                bot.send_message(message.chat.id, answer + "\n" + "\n" + description)
            else:
                answer = f"Hello {message.from_user.username}, you can use the commands below"
                bot.send_message(message.chat.id, answer + "\n" + "\n" + description)


    @bot.message_handler(commands=['Hello', 'hello'])
    def hello(message):
        answer = f"Hello {message.chat.username}"
        bot.send_message(message.chat.id, answer)


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
        dax_text = dax.get(request)
        tecdax_text = tecdax.get(request)
        sdax_text = sdax.get(request)
        mdax_text = mdax.get(request)
        dowjones_text = dowjones.get(request)
        nasdaq100_text = nasdaq100.get(request)
        if dax_text:
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
        ax1.set_title("Adjusted Close Price", color='black')

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
        
    @bot.message_handler(commands=['Crypto', 'crypto'])
    def get_crypto(message):
        markup_inline = types.InlineKeyboardMarkup()
        item_BTC = types.InlineKeyboardButton(text='BTC', callback_data='BTC')
        item_ETH = types.InlineKeyboardButton(text='ETH', callback_data='ETH')
        item_DOGE = types.InlineKeyboardButton(text='DOGE', callback_data='DOGE')
        item_XRP = types.InlineKeyboardButton(text='XRP', callback_data='XRP')
        markup_inline.add(item_BTC, item_ETH, item_DOGE, item_XRP)
        bot.send_message(message.chat.id, 'Choose a button to see the current Price', reply_markup=markup_inline)


    @bot.callback_query_handler(func=lambda call: True)
    def answer(call):
        if call.data == 'BTC':
            markup_reply = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            BTC_USD = types.InlineKeyboardButton('BTC-USD')
            BTC_EUR = types.InlineKeyboardButton('BTC-EUR')
            markup_reply.add(BTC_USD, BTC_EUR)
            bot.send_message(call.message.chat.id, 'Choose a currency', reply_markup=markup_reply)
        elif call.data == 'ETH':
            markup_reply = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            ETH_USD = types.InlineKeyboardButton('ETH-USD')
            ETH_EUR = types.InlineKeyboardButton('ETH-EUR')
            markup_reply.add(ETH_USD, ETH_EUR)
            bot.send_message(call.message.chat.id, 'Choose a currency', reply_markup=markup_reply)
        elif call.data == 'DOGE':
            markup_reply = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            DOGE_USD = types.InlineKeyboardButton('DOGE-USD')
            DOGE_EUR = types.InlineKeyboardButton('DOGE-EUR')
            markup_reply.add(DOGE_USD, DOGE_EUR)
            bot.send_message(call.message.chat.id, 'Choose a currency', reply_markup=markup_reply)
        elif call.data == 'XRP':
            markup_reply = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            XRP_USD = types.InlineKeyboardButton('XRP-USD')
            XRP_EUR = types.InlineKeyboardButton('XRP-EUR')
            markup_reply.add(XRP_USD, XRP_EUR)
            bot.send_message(call.message.chat.id, 'Choose a currency', reply_markup=markup_reply)


    @bot.message_handler(content_types=['text'])
    def get_text(message):
        if message.text == 'BTC-USD':
            ticker = 'BTC-USD'
            start = dt.datetime.now() - dt.timedelta(days=365)
            end = dt.datetime.now()
            data = web.DataReader(ticker, 'yahoo', start, end)
            price = data.iloc[-1]['Close']
            bot.send_message(message.chat.id, f'The current Price of {ticker} is {price} $', reply_markup=types.ReplyKeyboardRemove())
        elif message.text == 'BTC-EUR':
            ticker = 'BTC-EUR'
            start = dt.datetime.now() - dt.timedelta(days=365)
            end = dt.datetime.now()
            data = web.DataReader(ticker, 'yahoo', start, end)
            price = data.iloc[-1]['Close']
            bot.send_message(message.chat.id, f'The current Price of {ticker} is {price} €', reply_markup=types.ReplyKeyboardRemove())
        elif message.text == 'ETH-USD':
            ticker = 'ETH-USD'
            start = dt.datetime.now() - dt.timedelta(days=365)
            end = dt.datetime.now()
            data = web.DataReader(ticker, 'yahoo', start, end)
            price = data.iloc[-1]['Close']
            bot.send_message(message.chat.id, f'The current Price of {ticker} is {price} $', reply_markup=types.ReplyKeyboardRemove())
        elif message.text == 'ETH-EUR':
            ticker = 'ETH-EUR'
            start = dt.datetime.now() - dt.timedelta(days=365)
            end = dt.datetime.now()
            data = web.DataReader(ticker, 'yahoo', start, end)
            price = data.iloc[-1]['Close']
            bot.send_message(message.chat.id, f'The current Price of {ticker} is {price} €', reply_markup=types.ReplyKeyboardRemove())
        elif message.text == 'DOGE-USD':
            ticker = 'DOGE-USD'
            start = dt.datetime.now() - dt.timedelta(days=365)
            end = dt.datetime.now()
            data = web.DataReader(ticker, 'yahoo', start, end)
            price = data.iloc[-1]['Close']
            bot.send_message(message.chat.id, f'The current Price of {ticker} is {price} $', reply_markup=types.ReplyKeyboardRemove())
        elif message.text == 'DOGE-EUR':
            ticker = 'DOGE-EUR'
            start = dt.datetime.now() - dt.timedelta(days=365)
            end = dt.datetime.now()
            data = web.DataReader(ticker, 'yahoo', start, end)
            price = data.iloc[-1]['Close']
            bot.send_message(message.chat.id, f'The current Price of {ticker} is {price} €', reply_markup=types.ReplyKeyboardRemove())
        elif message.text == 'XRP-USD':
            ticker = 'XRP-USD'
            start = dt.datetime.now() - dt.timedelta(days=365)
            end = dt.datetime.now()
            data = web.DataReader(ticker, 'yahoo', start, end)
            price = data.iloc[-1]['Close']
            bot.send_message(message.chat.id, f'The current Price of {ticker} is {price} $', reply_markup=types.ReplyKeyboardRemove())
        elif message.text == 'XRP-EUR':
            ticker = 'XRP-EUR'
            start = dt.datetime.now() - dt.timedelta(days=365)
            end = dt.datetime.now()
            data = web.DataReader(ticker, 'yahoo', start, end)
            price = data.iloc[-1]['Close']
            bot.send_message(message.chat.id, f'The current Price of {ticker} is {price} €', reply_markup=types.ReplyKeyboardRemove())


    bot.infinity_polling()

