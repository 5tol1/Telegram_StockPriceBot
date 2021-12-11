import telebot
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
from telebot import types
import mysql.connector
import os

print("Bot started...")
BOT_TOKEN = os.environ.get("STOCKPRICE")
MYSQL = os.environ.get("MYSQL")
with daemon.DaemonContext():
    bot = telebot.TeleBot(BOT_TOKEN)

    my_db = mysql.connector.connect(host="127.0.0.1", user="your user", password=MYSQL, database="your Database")
    my_cursor = my_db.cursor() 

    @bot.message_handler(commands=['Help', 'help'])
    def send_help(message):
        if message.chat.type == "private" or "group":
            if message.chat.username == None:
                answer = f"Hello {message.from_user.first_name}, you can use the commands below"
                bot.send_message(message.chat.id, answer + "\n" + "\n" + description)
            else:
                answer = f"Hello {message.from_user.username}, you can use the commands below"
                bot.send_message(message.chat.id, answer + "\n" + "\n" + description)


    @bot.message_handler(commands=['Start', 'start'])
    def command_start(message):
        send_help(message)
   
    @bot.message_handler(commands=['Indices', 'indices'])
    def send_indices(message):        
        my_cursor.execute('SELECT * FROM indices')
        result = [i for i in my_cursor.fetchall()]
        final_result = "\n".join('  =  '.join((key, val)) for (key, val) in result)
        bot.send_message(message.chat.id, final_result)

    @bot.message_handler(commands=['Dax', 'dax'])
    def send_dax(message):
        my_cursor.execute('SELECT * FROM dax')
        result = [i for i in my_cursor.fetchall()]
        final_result = "\n".join('  =  '.join((key, val)) for (key, val) in result)
        bot.send_message(message.chat.id, final_result)


    @bot.message_handler(commands=['Mdax', 'mdax'])
    def send_mdax(message):
        my_cursor.execute('SELECT * FROM mdax')
        result = [i for i in my_cursor.fetchall()]
        final_result = "\n".join('  =  '.join((key, val)) for (key, val) in result)
        bot.send_message(message.chat.id, final_result)


    @bot.message_handler(commands=['Tecdax', 'tecdax'])
    def send_tecdax(message):
        my_cursor.execute('SELECT * FROM tecdax')
        result = [i for i in my_cursor.fetchall()]
        final_result = "\n".join('  =  '.join((key, val)) for (key, val) in result)
        bot.send_message(message.chat.id, final_result)


    @bot.message_handler(commands=['Sdax', 'sdax'])
    def send_sdax(message):
        my_cursor.execute('SELECT * FROM sdax')
        result = [i for i in my_cursor.fetchall()]
        final_result = "\n".join('  =  '.join((key, val)) for (key, val) in result)
        bot.send_message(message.chat.id, final_result)


    @bot.message_handler(commands=['Dowjones', 'dowjones'])
    def send_dowjones(message):
        my_cursor.execute('SELECT * FROM dowjones')
        result = [i for i in my_cursor.fetchall()]
        final_result = "\n".join('  =  '.join((key, val)) for (key, val) in result)
        bot.send_message(message.chat.id, final_result)


    @bot.message_handler(commands=['Nasdaq100', 'nasdaq100'])
    def send_nasdaq100(message):
        my_cursor.execute('SELECT * FROM nasdaq100')
        result = [i for i in my_cursor.fetchall()]
        final_result = "\n".join('  =  '.join((key, val)) for (key, val) in result)
        bot.send_message(message.chat.id, final_result)

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


    @bot.message_handler(commands=['Search', 'search'])
    def show_all_data(message):
        request = message.text.split()[1]
        final_request = request + '%'
        my_cursor.execute(f'SELECT * FROM stock WHERE company LIKE "{final_request}"')
        result = [i for i in my_cursor.fetchall()]
        final_result = "\n".join('  =  '.join((key, val)) for (key, val) in result)
        bot.send_message(message.chat.id, final_result)


    @bot.message_handler(commands=['Coin', 'coin'])
    def show_all_coin(message):
        request = message.text.split()[1]
        final_request = request + '%'
        my_cursor.execute(f'SELECT * FROM coin WHERE company LIKE "{final_request}"')
        result = [i for i in my_cursor.fetchall()]
        final_result = "\n".join('  =  '.join((key, val)) for (key, val) in result)
        bot.send_message(message.chat.id, final_result)

    @bot.message_handler(commands=['Get', 'get'])
    def send_getData(message):
        ua = UserAgent()
        header = {'User-Agent': str(ua.chrome)}
        request = message.text.split()[1].lower()
        url = f"https://finance.yahoo.com/quote/{request}"
        req = requests.get(url, headers=header)
        if req.status_code == 200:
            soup = BeautifulSoup(req.text, 'html.parser')
        else:
            print("Seite konnte nicht geladen werden.", url)

        stock = (soup.find('h1', {'class': 'D(ib) Fz(18px)'}).text + "\n" +
                 soup.find("div", {"class": "D(ib) Mend(20px)"}).find_all("fin-streamer")[0].text + "\n" +
                 soup.find("div", {"class": "D(ib) Mend(20px)"}).find_all("fin-streamer")[1].text + " " +
                 soup.find("div", {"class": "D(ib) Mend(20px)"}).find_all("fin-streamer")[2].text + "\n" +
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
        btc = types.InlineKeyboardButton(text='BTC', callback_data='BTC')
        eth = types.InlineKeyboardButton(text='ETH', callback_data='ETH')
        doge = types.InlineKeyboardButton(text='DOGE', callback_data='DOGE')
        xrp = types.InlineKeyboardButton(text='XRP', callback_data='XRP')
        markup_inline.add(btc, eth, doge, xrp)
        bot.send_message(message.chat.id, 'Choose a button for more options', reply_markup=markup_inline)


    @bot.callback_query_handler(func=lambda call: True)
    def answer(call):
        if call.data == 'BTC':
            markup_reply = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            btc_usd = types.InlineKeyboardButton('BTC USD')
            btc_eur = types.InlineKeyboardButton('BTC EUR')
            markup_reply.add(btc_usd, btc_eur)
            reply = bot.send_message(call.message.chat.id, 'Choose a currency', reply_markup=markup_reply)
            bot.register_next_step_handler(reply, markup_handler)
        elif call.data == 'ETH':
            markup_reply = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            eth_usd = types.InlineKeyboardButton('ETH USD')
            eth_eur = types.InlineKeyboardButton('ETH EUR')
            markup_reply.add(eth_usd, eth_eur)
            bot.send_message(call.message.chat.id, 'Choose a currency', reply_markup=markup_reply)
        elif call.data == 'DOGE':
            markup_reply = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            doge_usd = types.InlineKeyboardButton('DOGE USD')
            doge_eur = types.InlineKeyboardButton('DOGE EUR')
            markup_reply.add(doge_usd, doge_eur)
            bot.send_message(call.message.chat.id, 'Choose a currency', reply_markup=markup_reply)
        elif call.data == 'XRP':
            markup_reply = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            xrp_usd = types.InlineKeyboardButton('XRP USD')
            xrp_eur = types.InlineKeyboardButton('XRP EUR')
            markup_reply.add(xrp_usd, xrp_eur)
            bot.send_message(call.message.chat.id, 'Choose a currency', reply_markup=markup_reply)


    @bot.message_handler(content_types=['text'])
    def markup_handler(message):
        if message.text == 'BTC USD':
            markup_reply = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            btc_usd = types.InlineKeyboardButton('BTC $')
            btc_usd_high = types.InlineKeyboardButton('BTC High $')
            btc_usd_low = types.InlineKeyboardButton('BTC Low $')
            btc_usd_vol = types.InlineKeyboardButton('BTC Volume $')
            markup_reply.add(btc_usd, btc_usd_high, btc_usd_low, btc_usd_vol)
            reply = bot.send_message(message.chat.id, 'Choose', reply_markup=markup_reply)
            bot.register_next_step_handler(reply, get_text)
        elif message.text == 'BTC EUR':
            markup_reply = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            btc_eur = types.InlineKeyboardButton('BTC €')
            btc_eur_high = types.InlineKeyboardButton('BTC High €')
            btc_eur_low = types.InlineKeyboardButton('BTC Low €')
            btc_eur_vol = types.InlineKeyboardButton('BTC Volume €')
            markup_reply.add(btc_eur, btc_eur_high, btc_eur_low, btc_eur_vol)
            reply = bot.send_message(message.chat.id, 'Choose', reply_markup=markup_reply)
            bot.register_next_step_handler(reply, get_text)
        elif message.text == 'ETH USD':
            markup_reply = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            eth_usd = types.InlineKeyboardButton('ETH $')
            eth_usd_high = types.InlineKeyboardButton('ETH High $')
            eth_usd_low = types.InlineKeyboardButton('ETH Low $')
            eth_usd_vol = types.InlineKeyboardButton('BTC Volume $')
            markup_reply.add(eth_usd, eth_usd_high, eth_usd_low, eth_usd_vol)
            reply = bot.send_message(message.chat.id, 'Choose', reply_markup=markup_reply)
            bot.register_next_step_handler(reply, get_text)
        elif message.text == 'ETH EUR':
            markup_reply = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            eth_eur = types.InlineKeyboardButton('ETH €')
            eth_eur_high = types.InlineKeyboardButton('ETH High €')
            eth_eur_low = types.InlineKeyboardButton('ETH Low €')
            eth_eur_vol = types.InlineKeyboardButton('ETH Volume €')
            markup_reply.add(eth_eur, eth_eur_high, eth_eur_low, eth_eur_vol)
            reply = bot.send_message(message.chat.id, 'Choose', reply_markup=markup_reply)
            bot.register_next_step_handler(reply, get_text)
        elif message.text == 'DOGE USD':
            markup_reply = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            doge_usd = types.InlineKeyboardButton('DOGE $')
            doge_usd_high = types.InlineKeyboardButton('DOGE High $')
            doge_usd_low = types.InlineKeyboardButton('DOGE Low $')
            doge_usd_vol = types.InlineKeyboardButton('DOGE Volume $')
            markup_reply.add(doge_usd, doge_usd_high, doge_usd_low, doge_usd_vol)
            reply = bot.send_message(message.chat.id, 'Choose', reply_markup=markup_reply)
            bot.register_next_step_handler(reply, get_text)
        elif message.text == 'DOGE EUR':
            markup_reply = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            doge_eur = types.InlineKeyboardButton('DOGE €')
            doge_eur_high = types.InlineKeyboardButton('DOGE High €')
            doge_eur_low = types.InlineKeyboardButton('DOGE Low €')
            doge_eur_vol = types.InlineKeyboardButton('DOGE Volume €')
            markup_reply.add(doge_eur, doge_eur_high, doge_eur_low, doge_eur_vol)
            reply = bot.send_message(message.chat.id, 'Choose', reply_markup=markup_reply)
            bot.register_next_step_handler(reply, get_text)
        elif message.text == 'XRP USD':
            markup_reply = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            xrp_usd = types.InlineKeyboardButton('XRP $')
            xrp_usd_high = types.InlineKeyboardButton('XRP High $')
            xrp_usd_low = types.InlineKeyboardButton('XRP Low $')
            xrp_usd_vol = types.InlineKeyboardButton('XRP Volume $')
            markup_reply.add(xrp_usd, xrp_usd_high, xrp_usd_low, xrp_usd_vol)
            reply = bot.send_message(message.chat.id, 'Choose', reply_markup=markup_reply)
            bot.register_next_step_handler(reply, get_text)
        elif message.text == 'XRP EUR':
            markup_reply = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            xrp_eur = types.InlineKeyboardButton('XRP €')
            xrp_eur_high = types.InlineKeyboardButton('XRP High €')
            xrp_eur_low = types.InlineKeyboardButton('XRP Low €')
            xrp_eur_vol = types.InlineKeyboardButton('XRP Volume €')
            markup_reply.add(xrp_eur, xrp_eur_high, xrp_eur_low, xrp_eur_vol)
            reply = bot.send_message(message.chat.id, 'Choose', reply_markup=markup_reply)
            bot.register_next_step_handler(reply, get_text)


    def get_text(message):
        if message.text == 'BTC $':
            ticker = 'BTC-USD'
            start = dt.datetime.now() - dt.timedelta(days=365)
            end = dt.datetime.now()
            data = web.DataReader(ticker, 'yahoo', start, end)
            price = data.iloc[-1]['Close']
            bot.send_message(message.chat.id, f'The current Price of {ticker} is {price} $',
                             reply_markup=types.ReplyKeyboardRemove())
        elif message.text == 'BTC High $':
            ticker = 'BTC-USD'
            start = dt.datetime.now() - dt.timedelta(days=365)
            end = dt.datetime.now()
            data = web.DataReader(ticker, 'yahoo', start, end)
            high = data.iloc[-1]['High']
            bot.send_message(message.chat.id, f'The Highest Price of {ticker} today was {high} $',
                             reply_markup=types.ReplyKeyboardRemove())
        elif message.text == 'BTC Low $':
            ticker = 'BTC-USD'
            start = dt.datetime.now() - dt.timedelta(days=365)
            end = dt.datetime.now()
            data = web.DataReader(ticker, 'yahoo', start, end)
            low = data.iloc[-1]['Low']
            bot.send_message(message.chat.id, f'The Lowest Price of {ticker} today was {low} $',
                             reply_markup=types.ReplyKeyboardRemove())
        elif message.text == 'BTC Volume $':
            ticker = 'BTC-USD'
            start = dt.datetime.now() - dt.timedelta(days=365)
            end = dt.datetime.now()
            data = web.DataReader(ticker, 'yahoo', start, end)
            vol = data.iloc[-1]['Volume']
            bot.send_message(message.chat.id, f'The current Volume of {ticker} is {vol}',
                             reply_markup=types.ReplyKeyboardRemove())
        elif message.text == 'BTC €':
            ticker = 'BTC-EUR'
            start = dt.datetime.now() - dt.timedelta(days=365)
            end = dt.datetime.now()
            data = web.DataReader(ticker, 'yahoo', start, end)
            price = data.iloc[-1]['Close']
            bot.send_message(message.chat.id, f'The current Price of {ticker} is {price} €',
                             reply_markup=types.ReplyKeyboardRemove())
        elif message.text == 'BTC High €':
            ticker = 'BTC-EUR'
            start = dt.datetime.now() - dt.timedelta(days=365)
            end = dt.datetime.now()
            data = web.DataReader(ticker, 'yahoo', start, end)
            high = data.iloc[-1]['High']
            bot.send_message(message.chat.id, f'The Highest Price of {ticker} today was {high} €',
                             reply_markup=types.ReplyKeyboardRemove())
        elif message.text == 'BTC Low €':
            ticker = 'BTC-EUR'
            start = dt.datetime.now() - dt.timedelta(days=365)
            end = dt.datetime.now()
            data = web.DataReader(ticker, 'yahoo', start, end)
            low = data.iloc[-1]['Low']
            bot.send_message(message.chat.id, f'The Lowest Price of {ticker} today was {low} €',
                             reply_markup=types.ReplyKeyboardRemove())
        elif message.text == 'BTC Volume €':
            ticker = 'BTC-EUR'
            start = dt.datetime.now() - dt.timedelta(days=365)
            end = dt.datetime.now()
            data = web.DataReader(ticker, 'yahoo', start, end)
            vol = data.iloc[-1]['Volume']
            bot.send_message(message.chat.id, f'The current Volume of {ticker} is {vol}',
                             reply_markup=types.ReplyKeyboardRemove())
        elif message.text == 'ETH $':
            ticker = 'ETH-USD'
            start = dt.datetime.now() - dt.timedelta(days=365)
            end = dt.datetime.now()
            data = web.DataReader(ticker, 'yahoo', start, end)
            price = data.iloc[-1]['Close']
            bot.send_message(message.chat.id, f'The current Price of {ticker} is {price} $',
                             reply_markup=types.ReplyKeyboardRemove())
        elif message.text == 'ETH High $':
            ticker = 'ETH-USD'
            start = dt.datetime.now() - dt.timedelta(days=365)
            end = dt.datetime.now()
            data = web.DataReader(ticker, 'yahoo', start, end)
            high = data.iloc[-1]['High']
            bot.send_message(message.chat.id, f'The Highest Price of {ticker} today was {high} $',
                             reply_markup=types.ReplyKeyboardRemove())
        elif message.text == 'ETH Low $':
            ticker = 'ETH-USD'
            start = dt.datetime.now() - dt.timedelta(days=365)
            end = dt.datetime.now()
            data = web.DataReader(ticker, 'yahoo', start, end)
            low = data.iloc[-1]['Low']
            bot.send_message(message.chat.id, f'The Lowest Price of {ticker} today was {low} $',
                             reply_markup=types.ReplyKeyboardRemove())
        elif message.text == 'ETH Volume $':
            ticker = 'ETH-USD'
            start = dt.datetime.now() - dt.timedelta(days=365)
            end = dt.datetime.now()
            data = web.DataReader(ticker, 'yahoo', start, end)
            vol = data.iloc[-1]['Volume']
            bot.send_message(message.chat.id, f'The current Volume of {ticker} is {vol}',
                             reply_markup=types.ReplyKeyboardRemove())
        elif message.text == 'ETH €':
            ticker = 'ETH-EUR'
            start = dt.datetime.now() - dt.timedelta(days=365)
            end = dt.datetime.now()
            data = web.DataReader(ticker, 'yahoo', start, end)
            price = data.iloc[-1]['Close']
            bot.send_message(message.chat.id, f'The current Price of {ticker} is {price} €',
                             reply_markup=types.ReplyKeyboardRemove())
        elif message.text == 'ETH High €':
            ticker = 'ETH-EUR'
            start = dt.datetime.now() - dt.timedelta(days=365)
            end = dt.datetime.now()
            data = web.DataReader(ticker, 'yahoo', start, end)
            high = data.iloc[-1]['High']
            bot.send_message(message.chat.id, f'The Highest Price of {ticker} today was {high} €',
                             reply_markup=types.ReplyKeyboardRemove())
        elif message.text == 'ETH Low €':
            ticker = 'ETH-EUR'
            start = dt.datetime.now() - dt.timedelta(days=365)
            end = dt.datetime.now()
            data = web.DataReader(ticker, 'yahoo', start, end)
            low = data.iloc[-1]['Low']
            bot.send_message(message.chat.id, f'The Lowest Price of {ticker} today was {low} €',
                             reply_markup=types.ReplyKeyboardRemove())
        elif message.text == 'ETH Volume €':
            ticker = 'ETH-EUR'
            start = dt.datetime.now() - dt.timedelta(days=365)
            end = dt.datetime.now()
            data = web.DataReader(ticker, 'yahoo', start, end)
            vol = data.iloc[-1]['Volume']
            bot.send_message(message.chat.id, f'The current Volume of {ticker} is {vol}',
                             reply_markup=types.ReplyKeyboardRemove())
        elif message.text == 'DOGE $':
            ticker = 'DOGE-USD'
            start = dt.datetime.now() - dt.timedelta(days=365)
            end = dt.datetime.now()
            data = web.DataReader(ticker, 'yahoo', start, end)
            price = data.iloc[-1]['Close']
            bot.send_message(message.chat.id, f'The current Price of {ticker} is {price} $',
                             reply_markup=types.ReplyKeyboardRemove())
        elif message.text == 'DOGE High $':
            ticker = 'DOGE-USD'
            start = dt.datetime.now() - dt.timedelta(days=365)
            end = dt.datetime.now()
            data = web.DataReader(ticker, 'yahoo', start, end)
            high = data.iloc[-1]['High']
            bot.send_message(message.chat.id, f'The Highest Price of {ticker} today was {high} $',
                             reply_markup=types.ReplyKeyboardRemove())
        elif message.text == 'DOGE Low $':
            ticker = 'DOGE-USD'
            start = dt.datetime.now() - dt.timedelta(days=365)
            end = dt.datetime.now()
            data = web.DataReader(ticker, 'yahoo', start, end)
            low = data.iloc[-1]['Low']
            bot.send_message(message.chat.id, f'The Lowest Price of {ticker} today was {low} $',
                             reply_markup=types.ReplyKeyboardRemove())
        elif message.text == 'DOGE Volume $':
            ticker = 'DOGE-USD'
            start = dt.datetime.now() - dt.timedelta(days=365)
            end = dt.datetime.now()
            data = web.DataReader(ticker, 'yahoo', start, end)
            vol = data.iloc[-1]['Volume']
            bot.send_message(message.chat.id, f'The current Volume of {ticker} is {vol}',
                             reply_markup=types.ReplyKeyboardRemove())
        elif message.text == 'DOGE €':
            ticker = 'DOGE-EUR'
            start = dt.datetime.now() - dt.timedelta(days=365)
            end = dt.datetime.now()
            data = web.DataReader(ticker, 'yahoo', start, end)
            price = data.iloc[-1]['Close']
            bot.send_message(message.chat.id, f'The current Price of {ticker} is {price} €',
                             reply_markup=types.ReplyKeyboardRemove())
        elif message.text == 'DOGE High €':
            ticker = 'DOGE-EUR'
            start = dt.datetime.now() - dt.timedelta(days=365)
            end = dt.datetime.now()
            data = web.DataReader(ticker, 'yahoo', start, end)
            high = data.iloc[-1]['High']
            bot.send_message(message.chat.id, f'The Highest Price of {ticker} today was {high} €',
                             reply_markup=types.ReplyKeyboardRemove())
        elif message.text == 'DOGE Low €':
            ticker = 'DOGE-EUR'
            start = dt.datetime.now() - dt.timedelta(days=365)
            end = dt.datetime.now()
            data = web.DataReader(ticker, 'yahoo', start, end)
            low = data.iloc[-1]['Low']
            bot.send_message(message.chat.id, f'The Lowest Price of {ticker} today was {low} €',
                             reply_markup=types.ReplyKeyboardRemove())
        elif message.text == 'DOGE Volume €':
            ticker = 'DOGE-EUR'
            start = dt.datetime.now() - dt.timedelta(days=365)
            end = dt.datetime.now()
            data = web.DataReader(ticker, 'yahoo', start, end)
            vol = data.iloc[-1]['Volume']
            bot.send_message(message.chat.id, f'The current Volume of {ticker} is {vol}',
                             reply_markup=types.ReplyKeyboardRemove())
        elif message.text == 'XRP $':
            ticker = 'XRP-USD'
            start = dt.datetime.now() - dt.timedelta(days=365)
            end = dt.datetime.now()
            data = web.DataReader(ticker, 'yahoo', start, end)
            price = data.iloc[-1]['Close']
            bot.send_message(message.chat.id, f'The current Price of {ticker} is {price} $',
                             reply_markup=types.ReplyKeyboardRemove())
        elif message.text == 'XRP High $':
            ticker = 'XRP-USD'
            start = dt.datetime.now() - dt.timedelta(days=365)
            end = dt.datetime.now()
            data = web.DataReader(ticker, 'yahoo', start, end)
            high = data.iloc[-1]['High']
            bot.send_message(message.chat.id, f'The Highest Price of {ticker} today was {high} $',
                             reply_markup=types.ReplyKeyboardRemove())
        elif message.text == 'XRP Low $':
            ticker = 'XRP-USD'
            start = dt.datetime.now() - dt.timedelta(days=365)
            end = dt.datetime.now()
            data = web.DataReader(ticker, 'yahoo', start, end)
            low = data.iloc[-1]['Low']
            bot.send_message(message.chat.id, f'The Lowest Price of {ticker} today was {low} $',
                             reply_markup=types.ReplyKeyboardRemove())
        elif message.text == 'XRP Volume $':
            ticker = 'XRP-USD'
            start = dt.datetime.now() - dt.timedelta(days=365)
            end = dt.datetime.now()
            data = web.DataReader(ticker, 'yahoo', start, end)
            vol = data.iloc[-1]['Volume']
            bot.send_message(message.chat.id, f'The current Volume of {ticker} is {vol}',
                             reply_markup=types.ReplyKeyboardRemove())
        elif message.text == 'XRP €':
            ticker = 'XRP-EUR'
            start = dt.datetime.now() - dt.timedelta(days=365)
            end = dt.datetime.now()
            data = web.DataReader(ticker, 'yahoo', start, end)
            price = data.iloc[-1]['Close']
            bot.send_message(message.chat.id, f'The current Price of {ticker} is {price} €',
                             reply_markup=types.ReplyKeyboardRemove())
        elif message.text == 'XRP High €':
            ticker = 'XRP-EUR'
            start = dt.datetime.now() - dt.timedelta(days=365)
            end = dt.datetime.now()
            data = web.DataReader(ticker, 'yahoo', start, end)
            high = data.iloc[-1]['High']
            bot.send_message(message.chat.id, f'The Highest Price of {ticker} today was {high} €',
                             reply_markup=types.ReplyKeyboardRemove())
        elif message.text == 'XRP Low €':
            ticker = 'XRP-EUR'
            start = dt.datetime.now() - dt.timedelta(days=365)
            end = dt.datetime.now()
            data = web.DataReader(ticker, 'yahoo', start, end)
            low = data.iloc[-1]['Low']
            bot.send_message(message.chat.id, f'The Lowest Price of {ticker} today was {low} €',
                             reply_markup=types.ReplyKeyboardRemove())
        elif message.text == 'XRP Volume €':
            ticker = 'XRP-EUR'
            start = dt.datetime.now() - dt.timedelta(days=365)
            end = dt.datetime.now()
            data = web.DataReader(ticker, 'yahoo', start, end)
            vol = data.iloc[-1]['Volume']
            bot.send_message(message.chat.id, f'The current Volume of {ticker} is {vol}',
                             reply_markup=types.ReplyKeyboardRemove())


    bot.infinity_polling()
