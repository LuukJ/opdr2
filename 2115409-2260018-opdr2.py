#!/usr/bin/env python3
"""opdracht 2 - DeCode
Auteurs: Levi van Es  - 2115409
         Luuk de Jong - 2260018
Datum van laatste bewerking: 2018-10-25

Het programma kan tekst volgens het principe van
"Run-Length Encoding" coderen en decoderen en detecteert
daarbij getallen.
"""
import sys

INFOBLOKJE = \
"""
+-------------------------------------------------------------------+
|Auteurs:                                                           |
+- Naam: Levi van Es                                                |
|  Studentnummer: 2115409                                           |
|  Jaar van aankomst: 2018                                          |
|  Studierichting: Natuurkunde                                      |
|                                                                   |
+- Naam: Luuk de Jong                                               |
|  Studentnummer: 2260018                                           |
|  Jaar van aankomst: 2018                                          |
|  Studierichting: Natuurkunde                                      |
+-------------------------------------------------------------------+
|Opgave: DeCode                                                     |
+-------------------------------------------------------------------+
|Inleverdatum: 2018-10-26                                           |
+-------------------------------------------------------------------+
|Instructie voor gebruiker:                                         |
|    Er wordt gevraagd of er gecodeerd of gedecodeerd moet worden,  |
|    er wordt een invoerbestand en een uitvoerbestand gevraagd en   |
|    vervolgens wordt de inhoud van het invoerbestand gecodeerd     |
|    of gedecodeerd en weggeschreven naar het uitvoerbestand.       |
+-------------------------------------------------------------------+
"""


def encode(text):
    """Codeert tekst volgens Run-Length Encoding

    text - de te coderen tekst

    Tijdens het coderen worden getallen bijgehouden.
    Hoevaak deze getallen in bereiken [0,999], ..., [9000,9999]
    voorkomen wordt bijgehouden in de lijst `bins` teneinde het maken
    van een histogram.

    Retourneert de gecodeerde tekst en de bins voor het histogram.
    """
    out = ""
    i = 0
    getal = ""
    bins = [0]*10
    while i < len(text):
        n = 0
        char = text[i]
        while i < len(text) and text[i] == char:
            n += 1
            i += 1
        if char.isdigit():
            getal += char*n
        elif getal:
            if len(getal) < 5:
                bins[int(getal)//1000] += 1
            getal = ""
        if char in "\\0123456789":
            out += "\\"
        out += char
        if n > 1:
            out += str(n)
    if getal:
        bins[int(getal)//1000] += 1
    return out, bins


def palindroom(accu):
    """ retourneert (accu, reductions)

    accu - de accumulator van het decoderen

    Verwijdert het laatste cijfer tot het getal een palindroomgetal is
    en houdt daarbij in `reductions` bij hoevaak dit gebeurt.
    """
    string = str(accu)
    reductions = 0
    while string != string[::-1]:
        reductions += 1
        string = string[:-1]
    return accu, reductions


def histogram(bins):
    """Retourneert een histogram

    bins - een lijst van lengte 10 met daarin de frequenties van getallen
           binnen bereiken [0,999], [1000,1999], ..., [9000,9999].
 
    In de opdracht stond [1,999] i.p.v [0,999] maar [0,999] past beter
    bij de rest en op Blackboard staat dat 0 meetellen ook goed is.
    """
    rows = [["*" if bins[x]/max(bins)*10 > (y+0) else " " for x in range(10)]
            for y in range(10)]
    out = str(max(bins))
    for row in reversed(rows):
        out += "\n |" + " ".join(row)
    out += "\n +" + "-"*20
    out += "\n1" + " "*20 + "9999"
    return out


def decode(code):
    """ Decodeert de door `encode` gecodeerde tekst

    code - de gecodeerde tekst

    Tijdens het decoderen wordt op een aantal dingen gelet.
    Getallen die worden weggeschreven worden gedetecteerd en opgeteld
    bij een accumulator.
    Daarnaast wordt gelet op twee controlesequenties: ':R' en ':P'.
    ':R' reset de accumulator naar 0.
    ':P' voert een palindroombepaling uit (zie de functie `palindroom`)
    """
    i = 0  # positie in tekst
    escape = False  # Het volgende karakter letterlijk opvatten door backslash.
    digits = ""  # string voor bijhouden gedetecteerde getallen.
    n = 0  # Hoe vaak het karakter weg te schrijven is.
    prevletter = ""  # Het te onthouden karakter.
    out = ""  # De uiteindelijke uitvoer.
    accustring = ""  # String voor tijdelijke opslag getallen voor accumulator.
    accu = 0  # Accumulator
    while i <= len(code):
        if i < len(code):
            char = code[i]
        else:
            char = ""
        isescape = False
        if not escape and char.isdigit():
            digits += char
        elif not escape and char == "\\":
            isescape = True
        elif not escape and char == ":" and code[i+1] in "PR":
            n = int(digits or "1")
            digits = ""
            i += 1
            out += n*prevletter
            if prevletter.isdigit():
                accustring += prevletter*n
            accu += int(accustring or "0")
            accustring = ""
            prevletter = ""
            if code[i] == "R":
                accu = 0
                accustring = ""
            else:
                out += str(palindroom(accu)).replace(" ", "")
        else:
            n = int(digits or "1")
            digits = ""
            escape = False
            if prevletter.isdigit():
                accustring += prevletter*n
            else:
                accu += int(accustring or "0")
                accustring = ""
            out += n*prevletter
            prevletter = char
        escape = isescape
        i += 1
    if prevletter.isdigit():
        accustring += prevletter*n
    else:
        accu += int(accustring or "0")
        accustring = ""
    out += prevletter
    return out


def main():
    """Hoofdfunctie

    Toont de gebruiker het informatieblokje, vraagt om decoderen of coderen,
    een invoerbestand en een uitvoerbestand.
    Voert vervolgens de gekozen operatie uit op het invoerbestand en
    schrijft het weg naar het uitvoerbestand.
    Toont bij coderen de compressieverhouding en het aantal verwerkte regels
    en toont bij decoderen het histogram als dit zinvol is.
    """
    print(INFOBLOKJE)
    modus = "x"
    while modus not in "01":
        modus = input("Selecteer een operatie:\n[0] coderen\n[1] decoderen\n> ")
    f_in = None
    while not f_in:
        infile = input("Welk bestand lezen?\n> ")
        try:
            f_in = open(infile)
        except IOError:
            print(infile, "niet gevonden.")
    outfile = input("Opslaan als?\n> ")
    f_out = open(outfile, "w")
    if modus == "0":
        histogram_bins = [0 for _ in range(10)]
        outsize = 0
        insize = 0
        lines = 0
        for line in f_in:
            lines += 1
            # Veel unicode-karakters die buiten ASCII vallen zijn groter
            # dan 1 Byte
            insize += len(line.encode("utf8"))
            gecodeerd, bins = encode(line)
            outsize += len(gecodeerd.encode("utf8"))
            f_out.write(gecodeerd)
            for i in range(10):
                histogram_bins[i] += bins[i]
        print("Compressierate: {}%".format(outsize*100//insize))
        print("Regels verwerkt: {}".format(lines))
        if any(histogram_bins):
            print(histogram(histogram_bins))
    else:  # Het is al zeker dat modus ofwel 1 ofwerl 0 is.
        out = decode(f_in.read())
        f_out.write(out)
    f_out.close()
    f_in.close()
    return 0

if __name__ == "__main__":
    sys.exit(main())

