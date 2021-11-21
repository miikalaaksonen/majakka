import RPi.GPIO as GPIO
from time import sleep
from enum import Enum
import sys
import time
import random
from blinkstick import blinkstick


class Suunta(Enum):
    Myotapaivaan = 1
    Vastapaivaan = 2


class Vari(Enum):
    Keltainen = "FFFF00"
    Sininen = "0000FF"
    Punainen = "FF0000"
    Vihrea = "008000"
    Valkoinen = "FFFFFF"
    Purppura = "800080"
    Laivasto = "000080"
    Vesi = "00FFFF"
    Lime = "00FF00"
    Harmaa = "808080"


def LueNumero(teksti):
    if teksti.isdigit():
        return int(teksti,)
    else:
        return None


def VilkutaLed(portti1, portti2, nopeus):
    odota = (10-float(nopeus))*0.1
    jatka = True
    while (jatka):
        try:
            GPIO.output(portti1, GPIO.HIGH)
            GPIO.output(portti2, GPIO.LOW)
            time.sleep(odota)
            GPIO.output(portti1, GPIO.LOW)
            GPIO.output(portti2, GPIO.HIGH)
            time.sleep(odota)

        # press ctrl+c for keyboard interrupt
        except KeyboardInterrupt:
            GPIO.output(portti1, GPIO.LOW)
            GPIO.output(portti2, GPIO.LOW)
            jatka = False

def VihreaLed(portti1, portti2, nopeus):
            GPIO.output(portti1, GPIO.HIGH)
            GPIO.output(portti2, GPIO.LOW)

def PunainenLed(portti1, portti2, nopeus):
            GPIO.output(portti2, GPIO.HIGH)
            GPIO.output(portti1, GPIO.LOW)


def HTMLColorToRGB(colorstring):
    """ convert #RRGGBB to an (R, G, B) tuple """
    colorstring = colorstring.strip()
    if colorstring[0] == '#':
        colorstring = colorstring[1:]
    if len(colorstring) != 6:
        raise ValueError("input #%s is not in #RRGGBB format" % colorstring)
    r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:]
    r, g, b = [int(n, 16) for n in (r, g, b)]
    return [r, g, b]


def ValotPaalle(bstick, html):
    rgbVari = HTMLColorToRGB(html)
    for x in range(0, 8):
        bstick.set_color(channel=0, index=x,
                         red=rgbVari[0], green=rgbVari[1], blue=rgbVari[2])


def ValotPois(bstick):
    for x in range(0, 8):
        bstick.set_color(channel=0, index=x, red=0, green=0, blue=0)


def PyoritaMoottoria(portit, suunta, odota):
    if(suunta == Suunta.Myotapaivaan):
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

    elif(suunta == Suunta.Vastapaivaan):
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


def Pyorita(bstick, portit, suunta, nopeus, vari, aika, satunnainenVari, satunnainenNopeus, satunnainenSuunta):

    jatka = True
    kaytettyAika = 0
    varimuutosAika = 0
    nopeusmuutosAika = 0
    suuntamuutosAika = 0

    if(nopeus == 10):
        nopeus = 4

    ValotPaalle(bstick, vari.value)

    while jatka:
        try:
            if(satunnainenVari and (varimuutosAika + 3 < kaytettyAika)):
                varilista = list(map(lambda c: c.value, Vari))
                random.shuffle(varilista)
                ValotPaalle(bstick, varilista[0])
                varimuutosAika = kaytettyAika

            if(satunnainenNopeus and (nopeusmuutosAika + 3 < kaytettyAika)):
                nopeus = random.randint(1, 9)
                nopeusmuutosAika = kaytettyAika

            if(satunnainenSuunta and (suuntamuutosAika + 3 < kaytettyAika)):
                suuntalista = list(map(lambda c: c, Suunta))
                random.shuffle(suuntalista)
                suunta = suuntalista[0]
                suuntamuutosAika = kaytettyAika

            odota = (10-float(nopeus))/700

            if nopeus == 0:
                sleep(0.1)
            else:
                PyoritaMoottoria(portit, suunta, odota)
                kaytettyAika = kaytettyAika + (odota * 4)

                if kaytettyAika >= aika:
                    jatka = False

        # press ctrl+c for keyboard interrupt
        except KeyboardInterrupt:
            jatka = False
    
    ValotPois(bstick)


def OhjaaMajakkaa():
    mooottori_portit = (29, 31, 33, 35)
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(mooottori_portit, GPIO.OUT)

    ledPorttiPunainen = 10
    ledPorttiVihrea = 12
    GPIO.setup(ledPorttiPunainen, GPIO.OUT)
    GPIO.setup(ledPorttiVihrea, GPIO.OUT)

    PunainenLed(ledPorttiPunainen, ledPorttiVihrea, 7)

    # valitse suunta
    if len(sys.argv) > 1 and (sys.argv[1] == "v" or sys.argv[1] == "m" or sys.argv[1] == "s"):
        suuntaVastaus = sys.argv[1]
    else:
        suuntaVastaus = input(
            'Valitse pyörimissuunta v=vastapäivään, m=myötäpäivään, s = satunnainen: ')

    satunnainenSuunta = False
    if suuntaVastaus == "s":
        satunnainenSuunta = True

    if suuntaVastaus == "v":
        suunta = Suunta.Vastapaivaan
    else:
        suunta = Suunta.Myotapaivaan

    # valitse nopeus
    nopeus = None
    if len(sys.argv) > 2 and (sys.argv[2].isdigit()):
        nopeusArg = int(sys.argv[2])
        if nopeusArg >= 0 and nopeusArg <= 10:
            nopeus = nopeusArg

    if nopeus == None:
        nopeus = LueNumero(
            input('Valitse nopeus (0-9) 0=paikallaan, 9=nopea:, 10=satunnainen '))
        if nopeus == None:
            nopeus = 10

    # valitse väri
    if len(sys.argv) > 3:
        variVastaus = sys.argv[3]
    else:
        variVastaus = input(
            'Valitse väri sat=satunnainen, v=vihreä, s=sininen, k=keltainen, p=punainen:, <Enter> valkoinen: ')

    satunnainenVari = False
    if variVastaus == "sat":
        satunnainenVari = True

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

    #etsi valo
    bstick = blinkstick.find_first()
    #bstick = None
    if (bstick is None or nopeus is None):
        VilkutaLed(ledPorttiPunainen, ledPorttiVihrea, 7)
    else:
        VihreaLed(ledPorttiPunainen, ledPorttiVihrea, 7)
        Pyorita(bstick, mooottori_portit, suunta, nopeus, vari, 
                1000, satunnainenVari, nopeus == 10, satunnainenSuunta)

    PunainenLed(ledPorttiPunainen, ledPorttiVihrea, 7)


def Aloita():
    OhjaaMajakkaa()

if __name__ == "__main__":
    Aloita()
