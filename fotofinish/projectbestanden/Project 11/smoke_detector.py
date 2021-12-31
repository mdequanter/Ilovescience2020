#Project 11 - Gas- en rookmelder
#latest code updates available at: https://github.com/RuiSantosdotme/RaspberryPiProject
#project updates at: www.visualsteps.nl/raspberrypi/projectbestanden

#importeer de benodigde bibliotheken
from gpiozero import LED, Button, Buzzer, MCP3008
from time import sleep

led =  LED(17)
button = Button(2)
buzzer = Buzzer(27)
gas_sensor = MCP3008(0)

gas_sensor_status = False

threshold = 0.1

def arm_gas_sensor():
    global gas_sensor_status
    if gas_sensor_status == True:
        gas_sensor_status = False
        led.off()
    else:
        gas_sensor_status = True
        led.on()

button.when_pressed = arm_gas_sensor

while True:
    #print(gas_sensor.value)
    #controleer of de gassensor geactiveerd is en 
    #de drempelwaarde bereikt heeft
    if(gas_sensor_status == True and gas_sensor.value > threshold):
        buzzer.beep()
    else:
        buzzer.off()
    sleep(2)
