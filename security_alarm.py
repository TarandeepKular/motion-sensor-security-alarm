import RPi.GPIO as GPIO
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep
from datetime import date, datetime

buzzerPin = 11
sensorPin = 12
ledPin = 13

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(buzzerPin,GPIO.OUT)
GPIO.setup(sensorPin, GPIO.IN)
GPIO.setup(ledPin, GPIO.OUT)

myMQTTClient = AWSIoTMQTTClient("Alarm")
myMQTTClient.configureEndpoint("a348lsocmgokcp-ats.iot.us-west-2.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/home/pi/certs/Amazon-root-CA-1.pem", "/home/pi/certs/private.pem.key", "/home/pi/certs/certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1) 
myMQTTClient.configureDrainingFrequency(2) 
myMQTTClient.configureConnectDisconnectTimeout(10)  
myMQTTClient.configureMQTTOperationTimeout(5) 
myMQTTClient.connect()

state = 0
try:
    while True:
        
        time.sleep(0.1)
        state = GPIO.input(sensorPin)
        if state == 1:
            myMQTTClient.publish(
                topic= "Alert",
                QoS=0,
                payload="Motion detected")
            print ('Motion Detected')
            GPIO.output(buzzerPin,True)
            GPIO.output(ledPin,True)
            time.sleep(2)
            GPIO.output(buzzerPin,False)
            GPIO.output(ledPin,False)
            time.sleep(3)     
            
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
