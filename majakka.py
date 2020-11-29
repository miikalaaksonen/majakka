import RPi.GPIO as GPIO
from time import sleep
from enum import Enum
import sys
import time
from blinkstick import blinkstick


class Suunta(Enum):
    myotapaivaan = 1
    vastapaivaan = 2

class Vari(Enum):
    Keltainen = "FFFF00"
    Sininen = "0000FF"
    Punainen = "FF0000"
    Vihrea = "008000"
    Valkoinen = "FFFFFF"

def LueNumero(teksti):
 if teksti.isdigit():
  return int(teksti,)
 else:
  return None

def VilkutaLed(portti1,portti2, nopeus):
    odota = (10-float(nopeus))*0.1
    jatka = True
    while (jatka):
        try:
            GPIO.output(portti1,GPIO.HIGH)
            GPIO.output(portti2,GPIO.LOW)
            time.sleep(odota)
            GPIO.output(portti1,GPIO.LOW)
            GPIO.output(portti2,GPIO.HIGH)
            time.sleep(odota)

        # press ctrl+c for keyboard interrupt
        except KeyboardInterrupt:
            GPIO.output(portti1,GPIO.LOW)
            GPIO.output(portti2,GPIO.LOW)
            jatka = False

def HTMLColorToRGB(colorstring):
    """ convert #RRGGBB to an (R, G, B) tuple """
    colorstring = colorstring.strip()
    if colorstring[0] == '#': colorstring = colorstring[1:]
    if len(colorstring) != 6:
        raise ValueError("input #%s is not in #RRGGBB format" % colorstring)
    r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:]
    r, g, b = [int(n, 16) for n in (r, g, b)]
    return [r, g, b]

def ValotPaalle(bstick, html):
    rgbVari = HTMLColorToRGB(html)
    for x in range(0, 8):
        bstick.set_color(channel=0, index=x, red=rgbVari[0], green=rgbVari[1], blue=rgbVari[2])

def ValotPois(bstick):
    for x in range(0, 8):
        bstick.set_color(channel=0, index=x, red=0, green=0, blue=0)


def PyoritaMoottoria(suunta,nopeus,portit, aika):
    odota = (10-float(nopeus))/700
    jatka = True
    kaytettyAika = 0
    while jatka:
        try:
            if nopeus == 0:
                sleep(0.1)
            else:
                if(suunta == Suunta.myotapaivaan):
                    GPIO.output(portit, (GPIO.HIGH,
                                                GPIO.LOW, GPIO.LOW, GPIO.HIGH))
                    sleep(odota)
                    GPIO.output(portit, (GPIO.HIGH,
                                                GPIO.HIGH, GPIO.LOW, GPIO.LOW))
                    sleep(odota)
                    GPIO.output(portit, (GPIO.LOW,
                                                GPIO.HIGH, GPIO.HIGH, GPIO.LOW))
                    sleep(odota)
                    GPIO.output(portit, (GPIO.LOW,
                                                GPIO.LOW, GPIO.HIGH, GPIO.HIGH))
                    sleep(odota)

                elif(suunta == Suunta.vastapaivaan):
                    GPIO.output(portit, (GPIO.HIGH,
                                                GPIO.LOW, GPIO.LOW, GPIO.HIGH))
                    sleep(odota)
                    GPIO.output(portit, (GPIO.LOW,
                                                GPIO.LOW, GPIO.HIGH, GPIO.HIGH))
                    sleep(odota)
                    GPIO.output(portit, (GPIO.LOW,
                                                GPIO.HIGH, GPIO.HIGH, GPIO.LOW))
                    sleep(odota)
                    GPIO.output(portit, (GPIO.HIGH,
                                                GPIO.HIGH, GPIO.LOW, GPIO.LOW))
                    sleep(odota)
                kaytettyAika = kaytettyAika+ (odota * 4)
                if kaytettyAika >= aika:
                    jatka = False

        # press ctrl+c for keyboard interrupt
        except KeyboardInterrupt:
            jatka = False


# assign GPIO pins for motor
mooottori_portit = (29, 31, 33, 35)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
# for defining more than 1 GPIO channel as input/output use
GPIO.setup(mooottori_portit, GPIO.OUT)



ledPorttiPunainen = int(10)
ledPorttiVihrea = int(12)
GPIO.setup(ledPorttiPunainen,GPIO.OUT)
GPIO.setup(ledPorttiVihrea,GPIO.OUT)

# valitse suunta
if len(sys.argv) > 1 and (sys.argv[1] == "v" or sys.argv[1] == "m"):
    suuntaVastaus = sys.argv[1]
else:
    suuntaVastaus = input('Valitse pyörimissuunta v=vastapäivään, m=myötäpäivään: ')

if suuntaVastaus == "v":
    suunta = Suunta.vastapaivaan
elif suuntaVastaus == "m":
    suunta = Suunta.myotapaivaan
else:
    suunta = Suunta.myotapaivaan

#valitse nopeus
nopeus = None
if len(sys.argv) > 2 and (sys.argv[2].isdigit()):
    nopeusArg = int(sys.argv[2])
    if nopeusArg > 0 and nopeusArg < 10:
        nopeus = nopeusArg

if nopeus == None:
    nopeus = LueNumero(input('Valitse nopeus (0-9) 0=paikallaan, 9=nopea: '))

#valitse väri
if len(sys.argv) > 3:
    variVastaus = sys.argv[3]
else:
    variVastaus = input('Valitse väri v=vihreä, s=sininen, k=keltainen, p=punainen:, <Enter> valkoinen: ')

if variVastaus == "v":
    vari = Vari.Vihrea
elif variVastaus == "s":
    vari = Vari.Sininen
elif variVastaus == "k":
    vari = Vari.Keltainen
elif variVastaus == "p":
    vari = Vari.Punainen    
else:
    vari = Vari.Valkoinen

bstick = blinkstick.find_first()
if (bstick is None or nopeus is None):
    VilkutaLed(ledPorttiPunainen,ledPorttiVihrea,7)   
else:
    ValotPaalle(bstick,vari.value)
    PyoritaMoottoria(suunta,nopeus,mooottori_portit, 1000)
    #PyoritaMoottoria(Suunta.myotapaivaan,7,mooottori_portit, 3)
    #PyoritaMoottoria(Suunta.vastapaivaan,3,mooottori_portit, 5)
    #PyoritaMoottoria(Suunta.myotapaivaan,9,mooottori_portit, 2)
    #PyoritaMoottoria(Suunta.vastapaivaan,2,mooottori_portit, 4)

    ValotPois(bstick)
