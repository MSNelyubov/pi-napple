print("Beginning imports")
import time
import board
import adafruit_tcs34725
import adafruit_tca9548a
import busio
import digitalio
import sys
import RPi.GPIO as GPIO
print("disabling GPIO warnings")
GPIO.setwarnings(False)

print("Initializing GPIO channels...")
gpio_channels = [24,26,35,37]       #Channel number will be output pin number

print("setting GPIO mode to BOARD")
#GPIO.setmode(GPIO.BOARD)            #Sets mode to board numbering

print("setting up GPIO channels as outputs")
GPIO.setup(gpio_channels, GPIO.OUT, initial=GPIO.LOW) # sets up channels (GPIO pins) as an outputs for the motors



print("initializing i2c")
#initialize i2c 
i2c = busio.I2C(board.SCL, board.SDA)
#initialize multiplexor
print("initializing adafruit Mux")
tca = adafruit_tca9548a.TCA9548A(i2c)
#create sensor array
print("creating sensor array")
sensors = [0,0,0,0]
sensorsLux = [-1,-1,-1,-1]
sensors[0] = adafruit_tcs34725.TCS34725(tca[0]) #back right
sensors[1] = adafruit_tcs34725.TCS34725(tca[1]) #back left
sensors[2] = adafruit_tcs34725.TCS34725(tca[2]) #front left
sensors[3] = adafruit_tcs34725.TCS34725(tca[3]) #front right



def refreshSensorLux():
    print("refreshing sensors")
    str = ""
    n=0
    for i in range(4):
        lux = sensor.lux
        sensorsLux[i] = lux > 700
        lux = sensorsLux[i]
        str+=("s{0} Lux: {1}\t".format(n,lux))
        n= n+1
    print(sensorsLux)
    print(str)




def moveForward(n):
    GPIO.output(24, GPIO.HIGH)
    GPIO.output(35, GPIO.HIGH)
    GPIO.output(26, GPIO.LOW)
    GPIO.output(37, GPIO.LOW)
    time.sleep(n)
    GPIO.output(24, GPIO.LOW)
    GPIO.output(35, GPIO.LOW)

def moveBackward(n):
    GPIO.output(26, GPIO.HIGH)
    GPIO.output(37, GPIO.HIGH)
    GPIO.output(24, GPIO.LOW)
    GPIO.output(35, GPIO.LOW)
    time.sleep(n)
    GPIO.output(26, GPIO.LOW)
    GPIO.output(37, GPIO.LOW)


def turnRight(n):
    GPIO.output(35, GPIO.LOW)
    GPIO.output(37, GPIO.HIGH)
    GPIO.output(24, GPIO.HIGH)
    GPIO.output(26, GPIO.LOW)
    time.sleep(n)
    GPIO.output(26, GPIO.LOW)
    GPIO.output(37, GPIO.LOW)
    GPIO.output(26, GPIO.LOW)
    GPIO.output(37, GPIO.LOW)
    
def turnLeft(n):
    GPIO.output(35, GPIO.HIGH)
    GPIO.output(37, GPIO.LOW)
    GPIO.output(24, GPIO.LOW)
    GPIO.output(26, GPIO.HIGH)
    time.sleep(n)
    GPIO.output(26, GPIO.LOW)
    GPIO.output(37, GPIO.LOW)
    GPIO.output(26, GPIO.LOW)
    GPIO.output(37, GPIO.LOW)
    
    




print("beginning test loop")
refreshSensorLux()
while(sensorsLux[0] and sensorsLux[1]):
    turnLeft(0.01)
    refreshSensorLux()
moveBackward(0.1)

#while(sensors[0] > 1000 and sensors[1] > 1000 and sensors[2] > 1000 and sensors[3] > 1000)    #forward movement when no black tape detected
#    moveFordward(0.1)
#    refreshSensorLux()
#    
#if (sensors[2] < 1000 and sensors[3] < 1000 and sensors[1] > 1000) #turn left when tape ahead and not to the left
#    turnLeft(1)
#    refreshSensorLux()
#
#if (sensors[2] < 1000 and sensors[3] < 1000 and sensors[0] > 1000) #turn right when tape ahead and to the left
#    turnRight(1)
#    refreshSensorLux()
#    


GPIO.cleanup()