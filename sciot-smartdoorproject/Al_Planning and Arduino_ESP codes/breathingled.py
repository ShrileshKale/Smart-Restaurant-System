import requests
import RPi.GPIO as GPIO
import time
import sys
import os
import multiprocessing
import threading
from multiprocessing import Pool,Process
redLed = 12
def boardSetup():
	global breathingEffect
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(12,GPIO.OUT)
	GPIO.output(12,GPIO.LOW)
	breathingEffect = GPIO.PWM(redLed,1000)
	breathingEffect.start(0)
def breathing():
	global Breathing
	stop_thread = False
	if not stop_thread:
		while True:
			try:
				requests.get("https://google.com",timeout=3)
				for du in range(0, 101 , 4):
					breathingEffect.ChangeDutyCycle(du)
					time.sleep(0.05)
				time.sleep(1)
				for du in range (100, -1 , -4):
					breathingEffect.ChangeDutyCycle(du)
					time.sleep(0.05)
				time.sleep(1)
			except KeyboardInterrupt:
				breathingEffect.stop()
				stop_thread = True
				breathingEffect.stop()
				GPIO.output(redLed,GPIO.HIGH)
			except:
				print 'you got an error'
def breathingThread():
	Breathing = threading.Thread(target=breathing)
	Breathing.start()
	Breathing.join()

boardSetup()
breathingThread()
