#Part 0 - Pick a fruit
#latest code updates available at: https://github.com/RuiSantosdotme/RaspberryPiProject
#project updates at: https://nostarch.com/RaspberryPiProject

print('Kies een stuk fruit:')
print('aardbei, banaan of kiwi?')
color = input ('Voer de kleur in van het fruit dat je gekozen hebt: ')
if (color == 'rood'):
    print('Jouw fruit is een aardbei.')
elif (color == 'geel'):
    print('Jouw fruit is een banaan.')
elif (color == 'groen'):
    print('Jouw fruit is een kiwi.')
else:
    print('Ongeldige invoer.')
