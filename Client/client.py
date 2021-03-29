#-*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
import time
from tendo import singleton
from random import randint
import functions as func

me = singleton.SingleInstance()

reload(sys)  
sys.setdefaultencoding('utf8')

# main loop - waiting for commands					
while True:
	sys.stdout.flush() 
		
	# rec hot word
	recognizedText = func.transcribe(3)

	if len(recognizedText) > 0: 
		print time.strftime('%Y-%m-%d %H:%M:%S ')  + 'Recognized text: ' + recognizedText

	# assistant name detected
	if func.assistantNameDetected(recognizedText):
		func.play('beep.wav')

		# listen for voice command
		success = func.listenForCommand()	
		
		if not success:
			time.sleep(0.01)