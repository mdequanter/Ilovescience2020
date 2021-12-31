#Project 10 - Inbraakalarm met meldingen via e-mail
#latest code updates available at: https://github.com/RuiSantosdotme/RaspberryPiProject
#project updates at: www.visualsteps.nl/raspberrypi/projectbestanden

#importeer de benodigde bibliotheken
from gpiozero import LED, Button, MotionSensor
import smtplib
from email.mime.text import MIMEText
from signal import pause

#maak objecten die refereren aan elke led, de knop en de PIR-sensor
led_status = LED(17)
led_triggered = LED(18)
button = Button(2)
pir = MotionSensor(4)

#aansturen variabelen
motion_sensor_status = False
email_sent = False

#de PIR-sensor activeren of deactiveren
def arm_motion_sensor():
    global email_sent
    global motion_sensor_status
    if motion_sensor_status == True:
        motion_sensor_status = False
        led_status.off()
        led_triggered.off()
    else:
        motion_sensor_status = True
        email_sent = False
        led_status.on()

#e-mail verzenden wanneer beweging gedetecteerd is en de PIR-sensor geactiveerd is
def send_email():
    global email_sent
    global motion_sensor_status
    if(motion_sensor_status == True and email_sent == False):
        #vervang de volgende drie regels door je eigen toegangsgegevens
        from_email_addr = 'JE_E-MAILADRES@gmail.com'
        from_email_password = 'JE_E-MAIL_WACHTWOORD'
        to_email_addr = 'AAN_JE_ANDERE_E-MAILADRES@gmail.com'

        #stel het bericht voor je e-mail in
        body = 'Er is beweging gedetecteerd in je kamer.'
        msg = MIMEText(body)

        #stel de afzender en ontvanger in
        msg['Van'] = from_email_addr
        msg['Aan'] = to_email_addr

        #stel het onderwerp van je e-mail in
        msg['Onderwerp'] = 'INBRAAKALARM'

        #verbinden met de server en e-mail versturen
        #pas de volgende regel aan met de details van de SMTP-server van je provider
        server = smtplib.SMTP('smtp.gmail.com', 587)
        #verander de volgende regel van code naar opmerking als jouw e-mailprovider geen TLS gebruikt
        server.starttls()
        server.login(from_email_addr, from_email_password)
        server.sendmail(from_email_addr, to_email_addr, msg.as_string())
        server.quit()
        email_sent = True
        led_triggered.on()
        print('E-mail verzonden')

#wijs een functie toe die uitgevoerd wordt wanneer de knop ingedrukt wordt
button.when_pressed = arm_motion_sensor
#wijs een functie toe die uitgevoerd wordt wanneer beweging gedetecteerd wordt
pir.when_motion = send_email

pause()
