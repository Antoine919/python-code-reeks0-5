import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import csv


def heatmap_meerdere_maanden ():
    """Deze functie maakt een heatmap van elke maand en geeft een staafdiagram met de verschillen tussen de waarden van de satelliet en de lokale weerstations."""

    maanden_files = input("Geef alle namen van de bestanden, met de gegevens per maand, gescheiden door een komma: ").split(", ") #spatie moet er bij anders denkt dat de spatie voor de naam ook tot de naam behoort
    breedtegraden = input("Geef het bestand met de breedtegraden: ")
    lengtegraden = input("Geef het bestand met de lengtegraden: ")

    with open(breedtegraden) as breedtegraden:
        breedtegraden_lijst_lijst = list(csv.reader(breedtegraden))
        breedtegraden_lijst = []
        for element in breedtegraden_lijst_lijst:
            for coordinaat in element:
                breedtegraden_lijst.append(coordinaat)

    with open(lengtegraden) as lengte_graden:
        lengte_graden_lijst = list(csv.reader(lengte_graden))
        lengte_graden_lijst = lengte_graden_lijst[0]  #want lijsten in lijsten

    nummer = 0
    while 0 < 1 : # oneindige loop maken
        for maand in maanden_files:
            #plt.figure(maand) # zodat elke grafiek apart wordt afgebeeld
            df_maand = pd.read_csv(maand, names = lengte_graden_lijst)
            df_maand.index = breedtegraden_lijst
            if nummer == 0:                             # deze if lus is hier om ervoor te zorgen dat de colorbar niet elke keer geprint wordt, maar alleen de eerste keer en je een heel dunnen grafiek krijgt
                sns.heatmap(df_maand, cmap = "mako")
            else:
                sns.heatmap(df_maand, cmap="mako", cbar = False)
            plt.title(f"Sneeuwhoogte {maand[0:3]}")
            plt.show(block = False)         # zorgt ervoor dat de code niet stopt wanneer de figuur open staat
            plt.pause(1)                    # zorgt ervoor dat er x seconden wordt gewacht voor de plot te updaten, als time.sleep() gebruiken, wordt de plot niet volledig geladen voor een of andere reden
            nummer += 1
    plt.show()  #zorgt ervoor dat de figuren blijven openstaan

print(heatmap_meerdere_maanden())
#inputs:
"""
okt_Sentinel.csv, nov_Sentinel.csv, dec_Sentinel.csv, jan_Sentinel.csv, feb_Sentinel.csv
lat.csv
lon.csv
"""