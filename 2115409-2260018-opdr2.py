#!/usr/bin/env python3
"""opdracht 2 - DeCode
Auteurs: Levi van Es  - 2115409
         Luuk de Jong - 2260018
Datum van laatste bewerking: 2018-10-23

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
|  Studentnummer: 2115409                                                  |
|  Jaar van aankomst: 2018                                              |
|  Studierichting:                                                  |
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
            bins[int(getal)//1000] += 1
            getal = ""
        if char in "\\01234567890":
            out += "\\"
        out += char
        if n > 1:
            out += str(n)
    if getal:
        bins[int(getal)//1000] += 1
    return out, bins


def histogram(bins):
    rows = [["*" if bins[x]/max(bins)*10 > (y+0)  else " " for x in range(10)]
        for y in range(10)]
    out = str(max(bins))
    for row in reversed(rows):
        out += "\n |" + " ".join(row)
    out += "\n +" + "-"*20
    out += "\n1" + " "*20 + "9999"
    return out


def decode(code):
    i = 0
    escape = False
    digits = ""
    n = 0
    prevletter =""
    out = ""
    accustring = ""
    accu = 0
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
        elif not escape and char == ":":
            cmdchar = code[i+1]
            if cmdchar == "R":
                accu = 0
                prevletter = char
                accustring = ""
                i += 1
            elif char == "P":
                out += str(palindroom(accu)).replace(" ","")
                i += 1
            else:
                isescape = True
                i -= 1
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
        i+=1
    if prevletter.isdigit():
        accustring += prevletter*n
    else:
        accu += int(accustring or "0")
        accustring = ""
    out += prevletter
    return out, accu


def main():
    print(INFOBLOKJE)
    modus = "x"
    while modus not in "01":
        modus = input("Selecteer een operatie:\n[0] coderen\n[1] decoderen\n> ")
    f_in = None
    while not f_in:
        infile = input("Welk bestand lezen?\n> ")
        try:
            f_in = open(infile)
        except:
            print(infile, "niet gevonden.")
    outfile = input("Opslaan als?\n> ")
    uitvoer = ""
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
        return 0
    elif modus == "1":
        out, accu = decode(f_in.read())
        f_out.write(out)
        return 0
    
        



    f_out.close()
    f_in.close()
    return 0

if __name__ == "__main__":
    sys.exit(main())
