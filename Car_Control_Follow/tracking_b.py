import RPi.GPIO as GPIO
import time
import ultrasonic as us

IN1 = 20
IN2 = 21
IN3 = 19
IN4 = 26
ENA = 16
ENB = 13

TSLP1 = 3
TSLP2 = 5
TSRP1 = 4
TSRP2 = 18

chan_signal = True

L = 7


def init():
	global pwm_ENA
	global pwm_ENB
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(ENA,GPIO.OUT,initial=GPIO.HIGH)
	GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
	GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
	GPIO.setup(ENB,GPIO.OUT,initial=GPIO.HIGH)
	GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
	GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)
	GPIO.setup(TSLP1,GPIO.IN)
	GPIO.setup(TSLP2,GPIO.IN)
	GPIO.setup(TSRP1,GPIO.IN)
	GPIO.setup(TSRP2,GPIO.IN)

	GPIO.setup(L,GPIO.IN)

	pwm_ENA = GPIO.PWM(ENA,2000)
	pwm_ENB = GPIO.PWM(ENB,2000)
	pwm_ENA.start(0)
	pwm_ENB.start(0)
	
def run(leftspeed, rightspeed):
	GPIO.output(IN1,GPIO.HIGH)
	GPIO.output(IN2,GPIO.LOW)
	GPIO.output(IN3,GPIO.HIGH)
	GPIO.output(IN4,GPIO.LOW)
	pwm_ENA.ChangeDutyCycle(leftspeed)
	pwm_ENB.ChangeDutyCycle(rightspeed)
	
def back(leftspeed, rightspeed):
	GPIO.output(IN1,GPIO.LOW)
	GPIO.output(IN2,GPIO.HIGH)
	GPIO.output(IN3,GPIO.LOW)
	GPIO.output(IN4,GPIO.HIGH)
	pwm_ENA.ChangeDutyCycle(leftspeed)
	pwm_ENB.ChangeDutyCycle(rightspeed)

	
def brake():
	GPIO.output(IN1,GPIO.LOW)
	GPIO.output(IN2,GPIO.LOW)
	GPIO.output(IN3,GPIO.LOW)
	GPIO.output(IN4,GPIO.LOW)

def track(TSLV1,TSLV2,TSRV1,TSRV2):

	if TSLV1==0 and TSLV2==1 and TSRV1==1 and TSRV2==1:
		run(1,25)
	elif TSLV1==1 and TSLV2==0 and TSRV1==0 and TSRV2==1:
		run(10,10)
	elif TSLV1==1 and TSLV2==0 and TSRV1==1 and TSRV2==1:
		run(1,25)
	elif TSLV1==1 and TSLV2==1 and TSRV1==0 and TSRV2==1:
		run(20,1)
	elif TSLV1==1 and TSLV2==1 and TSRV1==1 and TSRV2==0:
		run(20,1)
	
	#time.sleep(0.01)
''' 
def track(): 
	if TSLV1==0 and TSLV2==0 and TSRV1==0 and TSRV2==0:
		back(0,20)
'''
def tri(order):
	if order == 'r':
		run(20,1)
		time.sleep(0.5)

	elif order == 'l':
		run(1,20)
		time.sleep(0.5)

	elif order == 'g':
		run(10,10)
		return
	while True:
		#time.sleep(0.2)
		TSLV1_tri = GPIO.input(TSLP1)
		TSLV2_tri = GPIO.input(TSLP2)
		TSRV1_tri = GPIO.input(TSRP1)
		TSRV2_tri = GPIO.input(TSRP2)
		if TSLV1_tri==1 and TSLV2_tri==0 and TSRV1_tri==0 and TSRV2_tri==1:
			return
	
def chan(order):
	run(7,7)
	time.sleep(1)
	if order == 'e':
		run(20,1)
		time.sleep(1)
	if order == 'q':
		run(1,30)
		time.sleep(1)
	global chan_signal
	chan_signal = False
	while 1:
		run(7,7)
		time.sleep(0.1)
		TSLV1_chan = GPIO.input(TSLP1)
		TSLV2_chan = GPIO.input(TSLP2)
		TSRV1_chan = GPIO.input(TSRP1)
		TSRV2_chan = GPIO.input(TSRP2)
		if not(TSLV1_chan and TSLV1_chan and TSRV1_chan and TSRV2_chan):
			return
 

def dou(order):
	
	if order == 'r':
		run(16,1)
	elif order == 'l':
		run(1,16)
	elif order == 'g':
		run(6,6)
	while True:
		
		#time.sleep(0.2)
		TSLV1_dou = GPIO.input(TSLP1)
		TSLV2_dou = GPIO.input(TSLP2)
		TSRV1_dou = GPIO.input(TSRP1)
		TSRV2_dou = GPIO.input(TSRP2)
		if TSLV1_dou==1 and TSLV2_dou==0 and TSRV1_dou==0 and TSRV2_dou==1:
			return
			



	
def tr(mode):
	order= mode
	global chan_signal
	TSLV1 = GPIO.input(TSLP1)
	TSLV2 = GPIO.input(TSLP2)
	TSRV1 = GPIO.input(TSRP1)
	TSRV2 = GPIO.input(TSRP2)
	#print(TSLV1,TSLV2,TSRV1,TSRV2)
	if GPIO.input(L) == 1:
		brake()
		time.sleep(0.01)
		return
	if mode =='q' or mode == 'e':
		if chan_signal:
			chan(mode)
		else:
			mode == 'g'
	if mode == 'g' or mode == 'l' or mode == 'r':
		chan_signal = True
	if not ((TSLV1==0 and TSLV2==0 and TSRV1==0 and TSRV2==0)or(TSLV1==1 and TSLV2==0 and TSRV1==0 and TSRV2==0)or(TSLV1==0 and TSLV2==0 and TSRV1==0 and TSRV2==1)):
		track(TSLV1,TSLV2,TSRV1,TSRV2)
	elif (TSLV1==0 and TSLV2==0 and TSRV1==0 and TSRV2==0) or (TSLV1==1 and TSLV2==0 and TSRV1==0 and TSRV2==0) or (TSLV1==0 and TSLV2==0 and TSRV1==0 and TSRV2==1):
		tri(order)
	'''
	elif TSLV1==1 and TSLV2==0 and TSRV1==0 and TSRV2==0:
		dou(order)
	elif TSLV1==0 and TSLV2==0 and TSRV1==0 and TSRV2==1:
		dou(order)
	'''
	
	