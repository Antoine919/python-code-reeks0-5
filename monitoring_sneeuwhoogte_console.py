from monitoring_sneeuwhoogte_deel_1 import aangepaste_gegevens
from monitoring_sneeuwhoogte_deel_2_mooi import plots_mooi


# Deel 1
print("Een bestand kuisen en samenvatten:", end = "\n")
locatie = input("Geef de bestandsnaam: ")
print()
print(aangepaste_gegevens(locatie, printen = True))
print()


# Deel 2
print("2 gebieden plotten:", end = "\n")
gebied_1 = input("Geef een eerste gebied: ")
bestand_1 = input("Geef het bestand van het eerste gebied: ")
gebied_2 = input("Geef een tweede gebied: ")
bestand_2 = input("Geef het bestand van het tweede gebied: ")
print()
plots_mooi(gebied_1, bestand_1, gebied_2, bestand_2)

# inputs:
"""
L'alpe de Vénosc
7589_datums_L'Alpe_de_Vénosc.csv
Courchevel
7893_datums_Courchevel.csv
"""