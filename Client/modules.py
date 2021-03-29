#-*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
import os
import psutil
import urllib2
import urllib
import json
from datetime import datetime
import commands
import feedparser
from bs4 import BeautifulSoup

import config as cfg
import voice_commands as voice
import functions as func

#check status
def status():
	cpuPercent = psutil.cpu_percent(interval=0.4)
	memoryPercent = psutil.virtual_memory()[2]
	
	msg = 'CPU usage: %s.' %cpuPercent
	msg += 'Memory usage: %s.' %memoryPercent
	
	return msg
 
# reboot
def reboot():
	func.say(voice.REBOOT_MSG)
	os.system('sudo reboot')

# shutdown	
def shutdown():
	func.say(voice.SHUTDOWN_MSG)
	os.system('sudo shutdown -h now')

# exit
def exit():
	func.say(voice.EXIT_MSG)
	sys.exit()
	
# time
def time():
	msg = 'Time is: ' + datetime.now().strftime('%H:%M:%S')
	func.say(msg)
								
# location
def loc():
	msg = ''
	
	try:
		apiUrl = 'http://ipinfo.io/json'
		response = urllib2.urlopen(apiUrl).read()
		jsonData = json.loads(response)	
	
		msg = 'Your current location is ' + jsonData['city'] + ', ' + jsonData['org']
	except:
		msg = cfg.API_ERROR_MSG
		
	func.say(msg)

# check coin price to fiat / btc
def checkCoinPrice(coin):
	apiUrl = 'https://min-api.cryptocompare.com/data/price?fsym=' + coin + '&tsyms=USD,BTC'
	try:
		response = urllib2.urlopen(apiUrl).read()
		jsonData = json.loads(response)

		return float(jsonData['USD']) 
	except:
		func.say(voice.API_ERROR_MSG)
		return ''

# check account balance
def checkAccountBalance():
	apiUrl = cfg.SERVER_API_URL + 'account'

	try:
		# get account balance from api (server)
		response = urllib2.urlopen(apiUrl).read()
		jsonData = json.loads(response)

		# say
		voiceMsg = 'Your balance is: ' + jsonData['balance_xym'] + ' XYM which is equivalent of $' + jsonData['balance_usd']
		func.say(voiceMsg)
	except:
		func.say(voice.API_ERROR_MSG)

# check last transaction
def checkLastTransaction():
	apiUrl = cfg.SERVER_API_URL + 'transaction/last'

	# get last transaction from api (server)
	response = urllib2.urlopen(apiUrl).read()
	jsonData = json.loads(response)

	#say
	voiceMsg = 'Last income transaction details. ' + 'Sender: ' +  jsonData['signer_name'] + '. Amount: ' + str(jsonData['amount_xym']) + ' XYM which is equivalent of $' + str(jsonData['amount_usd']) + '. Message: ' + jsonData['message']
	func.say(voiceMsg)

# check last message
def checkLastMessage():
	apiUrl = cfg.SERVER_API_URL + 'message/last'

	# get last transaction from api (server)
	response = urllib2.urlopen(apiUrl).read()
	jsonData = json.loads(response)

	#say
	voiceMsg = 'Last message details. ' + 'Sender: ' +  jsonData['signer_name'] + '. Message: ' + jsonData['message'] + '. Amount: ' + str(jsonData['amount_xym']) + ' XYM which is equivalent of $' + str(jsonData['amount_usd'])
	
	# print voiceMsg
	func.say(voiceMsg)

# send transaction
def sendTransaction():
	# select recipient (from saved contacts)
	func.say(voice.SELECT_RECIPIENT_MSG)
	recipient = func.transcribe(3)

	# select amount to send
	func.say(voice.SELECT_AMOUNT_MSG)
	amount = func.transcribe(3)

	# select message
	func.say(voice.SELECT_MESSAGE_MSG)
	message = func.transcribe(3)
	
	# if recipient and amount are not empty
	if recipient and amount:
		# confirm
		confirmVoiceMsg = ''
		if message:
			confirmVoiceMsg = 'Are you sure you want to send ' + str(amount) + ' XYM to ' + recipient + ' with message ' + message + '?'
		else:
			confirmVoiceMsg = 'Are you sure you want to send ' + str(amount) + ' XYM to ' + recipient + '?'

		func.say(confirmVoiceMsg) 
		confirm = func.transcribe(3)

		# if configm, send transaction
		if confirm == 'Yes':
			# gen url to api (server)
			apiUrl = cfg.SERVER_API_URL + 'transaction/send/' + recipient + '/' + str(amount) + '/' + message.replace(' ', '%20')	
			func.say(voice.TRANSACION_SENDED_MSG)

			# send transaction and wait for confirmation
			response = urllib2.urlopen(apiUrl).read()
			jsonData = json.loads(response)

			# say confirmation
			voiceMsg = 'Transaction confirmed. Now your balance is: ' + jsonData['balance_xym'] + ' XYM which is equivalent of $' + jsonData['balance_usd']
			func.say(voiceMsg)
		else:
			func.say(voice.TRANSACTION_NOT_SENDED_MSG)
	else:
		func.say(voice.SEND_TRANSACTION_NOT_UNDERSTAND_MSG)