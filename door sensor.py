import RPi.GPIO as GPIO
import time
from gpiozero import *
from time import sleep
from sinchsms import SinchSMS

red = LED(2)
green = LED(3)
GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
sensor = DistanceSensor(echo=19,trigger=20)

def sendSMS():
    global message
    username = 'username'
    password = 'password'
    number = '###'
    app_key = 'app_key'
    app_secret = 'app_secret'

    message=""

    client = SinchSMS(app_key, app_secret)
    print("Sending '%s' to %s" % (message, number))

    response = client.send_message(number, message)
    message_id = response['messageId']
    response = client.check_status(message_id)

    # keep trying unless the status returned is Successful
    while response['status'] != 'Successful':
        print(response['status'])
        time.sleep(1)
        response = client.check_status(message_id)

    print(response['status'])

if __name__ == "__main__":
    sendSMS()

lm="closed."
om="open."
while True:
    distance = sensor.distance * 100
    print ("distance:  %.lf" % distance)
    sleep(1)
    if GPIO.input(14) == GPIO.HIGH:
        if distance <= 5:
            message=+ lm
            red.off()
            green.on()
            sendSMS()
        elif distance >5:
            message=+cm
            green.off()
            red.on()
            sendSMS()

    elif GPIO.input(14) == GPIO.LOW:
        green.off()
        red.off()