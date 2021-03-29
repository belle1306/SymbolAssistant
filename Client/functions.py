#-*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
import os
from os import path
import speech_recognition as sr
import subprocess
import time
from subprocess import Popen, PIPE, STDOUT
import urllib2
import json
import HTMLParser
from random import randint

import config as cfg
import voice_commands as voice
import modules as mod

# say msg
def say(text):
	subprocess.call([cfg.BASE_DIR + "speech.sh", text])

def recognizedTextHasCmd(recognizedText, cmd):
	return recognizedText.lower().find(cmd) > -1

#check if assistant name detected
def assistantNameDetected(recognizedText):
	return recognizedTextHasCmd(recognizedText, voice.ASSISTANT_NAME)

# play file
def play(file):
	# os.system('aplay -q ' + cfg.AUDIO_DIR + file)
	os.system('aplay -q -D plughw:1,0 ' + cfg.AUDIO_DIR + file) #usb card
			
def _playRandom(array):
	file = random.choice(array)
	os.system('aplay -q ' + cfg.AUDIO_DIR + file)
			
def playRandom(voice, count):
	file = voice + str(randint(1, count)) + '.wav'
	play(file)
    
def transcribe(duration):
	filename = cfg.AUDIO_DIR + 'test.wav'
	# Sleep if music playing
	if isAudioPlaying():
		return ""

	# Record voice sample
	os.system('arecord -D plughw:1,0 -f cd -c 1 -t wav -d ' + str(duration) + '  -q -r 16000 ' + filename)
	
	# Check if audio sample is loud enough
	cmd = 'sox ' + filename + ' -n stat'
	p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
	soxOutput = p.stdout.read()
	maxAmpStart = soxOutput.find("Maximum amplitude")+24
	maxAmpEnd = maxAmpStart + 7
	maxAmpValueText = soxOutput[maxAmpStart:maxAmpEnd]
	print "Max amplitude: " + maxAmpValueText
	maxAmpValue = float(maxAmpValueText)
	time.sleep(0.05)

	if (maxAmpValue < 0.3) :
		# Audio sample is too quiet
		return ""	

	AUDIO_FILE = path.join(cfg.AUDIO_DIR, "test.wav")

	r = sr.Recognizer()
	with sr.AudioFile(AUDIO_FILE) as source:
		audio = r.record(source)

	# Send sample to google	
	try:
		final_result = r.recognize_google(audio, language=cfg.LANG)
		print("Recognized text: " + final_result)
	except sr.UnknownValueError:
		print("Text could not be recognized")
		final_result = ""
	except sr.RequestError as e:
		print("Error occured: {0}".format(e))
		final_result = ""

	return final_result    

# Check if audio is playing    
def isAudioPlaying():	
	audioPlaying = False 

	cmd = 'ps -C omxplayer,mplayer'
	lineCounter = 0
	p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)

	for ln in p.stdout:
		lineCounter = lineCounter + 1
		
		if lineCounter > 1:
			audioPlaying = True
			break

	return audioPlaying ; 

# Listen for voice command
def listenForCommand(): 	
	command = transcribe(3)
	
	print time.strftime("%Y-%m-%d %H:%M:%S ")  + "Command: <" + command + ">"		
	success = True		
			
	#status
	if recognizedTextHasCmd(command, voice.STATUS_CMD):
		say(mod.status())
	#thx
	elif recognizedTextHasCmd(command, voice.THX_CMD):
		say(voice.THX_MSG)
	#reboot
	elif recognizedTextHasCmd(command, voice.REBOOT_CMD):
		mod.reboot()
	#shutdown
	elif recognizedTextHasCmd(command, voice.SHUTDOWN_CMD):
		mod.shutdown()	
	#exit
	elif recognizedTextHasCmd(command, voice.EXIT_CMD):
		mod.exit()    
	#time
	elif recognizedTextHasCmd(command, voice.TIME_CMD): 
		mod.time()
	#loc
	elif recognizedTextHasCmd(command, voice.LOC_CMD): 
		mod.loc()	
	#account balance
	elif recognizedTextHasCmd(command, voice.ACCOUNT_BALANCE_CMD):
		mod.checkAccountBalance()
	#check last transaction
	elif recognizedTextHasCmd(command, voice.LAST_TRANSACTION_CMD):
		mod.checkLastTransaction()
	#check last message
	elif recognizedTextHasCmd(command, voice.LAST_MESSAGE_CMD):
		mod.checkLastMessage()
	#beep
	elif command == '':
		play('beep.wav')
	#unrecognized command
	else:
		if command != '':
			say(voice.DONT_UNDERSTAND_MSG)
			success = False

	return success