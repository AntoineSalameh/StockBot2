import discord
import io
import os
import requests
import json
import finnhub
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import pandas as pd
import numpy as np
from urllib.request import urlopen
from keep_alive import keep_alive

client = discord.Client()

finnhub_client = finnhub.Client(api_key=os.getenv('FinnToken'))
#to keep the token secured we have it in a .env file 
#and use the method getenv to place the token where needed
      
  
bot = commands.Bot(command_prefix= '$')



#print(finnhub_client.aggregate_indicator('AAPL', 'D'))
#print(finnhub_client.company_basic_financials('AAPL', 'margin'))
#print(finnhub_client.company_news('AAPL', _from="2020-06-01", to="2020-06-10"))
#print(finnhub_client.forex_symbols('OANDA'))
#print(finnhub_client.general_news('forex', min_id=0))
#print(finnhub_client.quote('AAPL'))
#print(finnhub_client.stock_symbols('US')[0:5])
#print(finnhub_client.symbol_lookup('apple'))
#print(finnhub_client.recommendation_trends('AAPL'))
#print(finnhub_client.company_profile2(symbol='AAPL'))

@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.online, activity=discord.Game('STONKS | $help'))

  #the line above is related to discord pov

  print('We have logged in as {0.user}'.format(client))

  #to print in console to know when the bot is on
  

@client.event
async def on_message(message):
  
  #if message.channel.id != channelId:
  #  return
  #the lines above are to make the bot work exclusively in a predefined discord channel

  #we need to make sure the bot don't reply to itself
  if message.author == client.user:
    return

  msg = message.content
  
  if msg.startswith('$search'):
    symbol = msg.split("$search ",1)[1]
    finnhub_client.symbol_lookup(symbol)
    r = requests.get('https://finnhub.io/api/v1/search?q='+ symbol + '&token='+ os.getenv('FinnToken'))
    data = r.json()
    result = np.array(data)
    print(result)
    #for i in result:
    #  desc = {result['description']}
    #  print (desc)
    s = f''' Results count = {data['count']}\nResults:\n {data['result']} '''
    await message.channel.send(s)
    #res = pd.DataFrame(r.json())
    #await message.channel.send(res)

  if msg.startswith('$help'):
    cmdhelp = msg.split("$help",1)[1]
    if cmdhelp == "":
      command ="Hello friend! Here are the commands:\n$quote 'symbol' (ex: $quote AAPL)\nOr you can use it as 'Quote $<symbol>' (ex:Quote $bbkcf)\n$profile 'symbol' (ex: $profile BBBY)\n$hello\n$ping\nIf you need help with a specific command use $help 'command' (ex: $help quote)\nAnd if the bot replies with 0s or just {}, most likely the stock symbol isn't valid."
      await message.channel.send(command)

    if cmdhelp == " hello":
      expl = "This command is just to make sure the bot is still working in case it didn't respond previously."
      await message.channel.send(expl)

    if cmdhelp == " ping":
      expl = "Pong. Yeah the bot is based on memes."
      await message.channel.send(expl)

    if cmdhelp == " quote":
      expl = "This command get real-time quote data for US stocks.\n(c) stands for Current price\n(h) stands for High price of the day\n(l) stands for Low price of the day\n(o) stands for Open price of the day\n(pc) stands for Previous close price\n(t) stands for UNIX milliseconds timestamp."
      await message.channel.send(expl)
    #print("(c) stands for current price")
    #print("(h) stands for highest")
    #print("(l) stands for lowest")
    #print("(o) stands for opening price")
    #print("(pc) stands for previous closure")
    #print("(t) stands for UNIX milliseconds timestamp.")
    
    if cmdhelp == " profile":
      expl = "This command get general information of a company:\nCountry of company's headquarter, currency used in company filings, listed exchange, industry classification, IPO date, market capitalization, company name, number of oustanding shares, company symbol/ticker as used on the listed exchange and company website."
      await message.channel.send(expl)

  if msg.startswith('Quote'):
    symbol = msg.split("Quote $",1)[1]
    if symbol.islower() == True:
      symbol = symbol.upper()
      finnhub_client.quote(symbol)
      r = requests.get('https://finnhub.io/api/v1/quote?symbol='+ symbol +'&token='+ os.getenv('FinnToken'))
      data = r.json()
      s = f''' Current stock price c = {data['c']}\nHigh price of the day h = {data['h']}\nLow price of the day l = {data['l']}\nOpen price of the day o = {data['o']}\nPrevious close price pc = {data['pc']} '''
      await message.channel.send(s)
      #await message.channel.send(r.json()) old version
    else:
      finnhub_client.quote(symbol)
      r = requests.get('https://finnhub.io/api/v1/quote?symbol='+ symbol +'&token='+ os.getenv('FinnToken'))
      data = r.json()
      s = f''' Current stock price c = {data['c']}\nHigh price of the day h = {data['h']}\nLow price of the day l = {data['l']}\nOpen price of the day o = {data['o']}\nPrevious close price pc = {data['pc']} '''
      await message.channel.send(s)
      #await message.channel.send(r.json())


  if msg.startswith('$quote'):
    symbol = msg.split("$quote ",1)[1]

    #making sure we don't get errors when typing 
    #the quote symbol in lowercase letters

    if symbol.islower() == True:
      symbol = symbol.upper()
      finnhub_client.quote(symbol)
      r = requests.get('https://finnhub.io/api/v1/quote?symbol='+ symbol +'&token='+ os.getenv('FinnToken'))
      #print(r.json())
      #it was to make sure in the console
      data = r.json()
      #if ({data['c']}>{data['l']}):
      #  sign = '+Stonks'
      #else:
      #  sign = '-NotStonk'
      s = f''' Current stock price c = {data['c']}\nHigh price of the day h = {data['h']}\nLow price of the day l = {data['l']}\nOpen price of the day o = {data['o']}\nPrevious close price pc = {data['pc']} '''
      await message.channel.send(s)
      #await message.channel.send(r.json())
    
    #if it's already in uppercase we leave it as it is

    else:
      finnhub_client.quote(symbol)
      r = requests.get('https://finnhub.io/api/v1/quote?symbol='+ symbol +'&token='+ os.getenv('FinnToken'))
      #print(r.json())
      data = r.json()
      s = f''' Current stock price c = {data['c']}\nHigh price of the day h = {data['h']}\nLow price of the day l = {data['l']}\nOpen price of the day o = {data['o']}\nPrevious close price pc = {data['pc']} '''
      await message.channel.send(s)
      #await message.channel.send(r.json())
    
    
    #finnhub_client.quote(symbol)
    #r = requests.get('https://finnhub.io/api/v1/quote?symbol='+ symbol +'&token='+ os.getenv('FinnToken'))
    #print(r.json())
    #await message.channel.send(r.json())

  if msg.startswith('$profile'):
    symbol = msg.split("$profile ",1)[1]
    
    #making sure of the writing as mentioned before

    if symbol.islower() == True:
      symbol = symbol.upper()
      finnhub_client.company_profile2()
      r = requests.get('https://finnhub.io/api/v1/stock/profile2?symbol='+ symbol +'&token='+ os.getenv('FinnToken'))
      #print(r.json())
      data = r.json()
      s = f''' Company name: {data['name']}\nIndustry category: {data['finnhubIndustry']} \nCountry: {data['country']}\nWebsite: {data['weburl']}\nIPO: {data['ipo']}\nTicker: {data['ticker']}\nCurrency: {data['currency']}\nListed exchange: {data['exchange']}\nMarket capitalization: {data['marketCapitalization']}\nShare oustanding: {data['shareOutstanding']} '''
      await message.channel.send(s)
      #await message.channel.send(r.json())

    #else as mentioned before for uppercase letters

    else:
      finnhub_client.company_profile2()
      r = requests.get('https://finnhub.io/api/v1/stock/profile2?symbol='+ symbol +'&token='+ os.getenv('FinnToken'))
      #print(r.json())
      data = r.json()
      s = f''' Company name: {data['name']}\nIndustry category: {data['finnhubIndustry']} \nCountry: {data['country']}\nWebsite: {data['weburl']}\nIPO: {data['ipo']}\nTicker: {data['ticker']}\nCurrency: {data['currency']}\nListed exchange: {data['exchange']}\nMarket capitalization: {data['marketCapitalization']}\nShare oustanding: {data['shareOutstanding']} '''
      await message.channel.send(s)
      #await message.channel.send(r.json())

  #adding a command "hello" to make sure
  #the bot still working

  if msg.startswith('$hello'):
    hello = "Hello trader, hope your day going aight"
    await message.channel.send(hello)

  if msg.startswith('$ping'):
    pong = "Pong!"
    await message.channel.send(pong)

  #if msg.startswith('$exchange'):
  #  r = requests.get('https://finnhub.io/api/v1/crypto/exchange?token='+ os.getenv('FinnToken'))
  #  print(r.json())
  #  await message.channel.send(r.json())




    


keep_alive()
client.run(os.getenv('TOKEN'))
