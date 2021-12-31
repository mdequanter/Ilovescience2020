#Project 10 - Inbraakalarm met meldingen via e-mail - Send Email
#latest code updates available at: https://github.com/RuiSantosdotme/RaspberryPiProject
#project updates at: ww.visualsteps.nl/raspberrypi/projectbestanden

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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

#set your email subject
msg['Onderwerp'] = 'INBRAAKALARM'

#verbinden met de server en e-mail versturen
#pas de volgende regel aan met de details van de SMTP-server van je provider
server = smtplib.SMTP('smtp.gmail.com', 587)
#verander de volgende regel van code naar opmerking als jouw e-mailprovider geen TLS gebruikt
server.starttls()
server.login(from_email_addr, from_email_password)
server.sendmail(from_email_addr, to_email_addr, msg.as_string())
server.quit()
print('E-mail verzonden')
