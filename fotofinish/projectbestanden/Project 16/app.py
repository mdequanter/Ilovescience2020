#Project 16 - Je elektronica met het web verbinden
#latest code updates available at: https://github.com/RuiSantosdotme/RaspberryPiProject
#project updates at: www.visualsteps.nl/raspberrypi/projectbestanden

#importeer de benodigde bibliotheken
from gpiozero import LED
from flask import Flask, render_template, request

#maak een Flask object
app = Flask(__name__)

#maak een object dat refereert aan een relais
relay = LED(17)
#stel het relais in op uit; denk eraan dat het relais met inverted logic werkt
relay.on()
#sla de huidige status van het relais op
relay_state = 'Relay is uit'

#geef de webpagina weer
@app.route('/')
def main():
   global relay_state
   #geef de status van het relais door aan index.html en retourneer dit aan de gebruiker
   return render_template('index.html', relay_state=relay_state)

#voer control() uit als iemand de aan-/uitknoppen indrukt
@app.route('/<action>')
def control(action):
   global relay_state
   #als het action deel van de URL 'aan' is, zet dan het relais aan
   if action == 'on':
      #zet het relais aan
      relay.off()
      #sla de status van het relais op 
      relay_state = 'Relay is aan'
   if action == 'off':
      relay.on()
      relay_state = 'Relay is uit'

   # geef de status van het relais door aan index.html en retourneer dit aan de gebruiker
   return render_template('index.html', relay_state=relay_state)

#start de webserver op localhost op poort 80
if __name__ == '__main__':
   app.run(host='0.0.0.0', port=80, debug=True)
