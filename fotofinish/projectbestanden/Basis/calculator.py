#Part 0 - Python Calculator
#latest code updates available at: https://github.com/RuiSantosdotme/RaspberryPiProject
#project updates at: https://www.visualsteps.nl/raspberrypi/projectbestanden

running = True
welcome_message = '***Welkom bij de Python-calculator***'
print(welcome_message)
while running:
    print('Bewerkingen')
    print('1 = Optellen')
    print('2 = Aftrekken')
    print('3 = Vermenigvuldigen')
    print('4 = Delen')
    print('5 = Programma afsluiten')
    operation = int(input('Voer een getal in om een bewerking te kiezen: '))
    if operation == 1:
        print('Optellen')
        first = int(input('Voer het eerste getal in: '))
        second = int(input('Voer het tweede getal in: '))
        print('Uitkomst = ', first + second)
    elif operation == 2:
        print('Aftrekken')
        first = int(input('Voer het eerste getal in: '))
        second = int(input('Voer het tweede getal in: '))
        print('Uitkomst =  ', first - second)
    elif operation == 3:
        print('Vermenigvuldigen')
        first = int(input('Voer het eerste getal in: '))
        second = int(input('Voer het tweede getal in: '))
        print('Uitkomst = ', first * second)
    elif operation == 4:
        print('Delen')
        first = int(input('Voer het eerste getal in: '))
        second = int(input('Voer het tweede getal in: '))
        print('Uitkomst = ', first / second)
    elif operation == 5:
        print('Het programma afsluiten... ')
        running = False
