import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import csv
import numpy as np
from monitoring_sneeuwhoogte_deel_1 import aangepaste_gegevens
from monitoring_sneeuwhoogte_deel_3 import sneeuwhoogte_sat


def verschil_staafdiagram_slecht (station_C, station_A, lat, lon, *maanden):
    """Deze functie geeft een staafdiagram met de verschillen tussen de waarden van de satelliet en de lokale
weerstations, maar deze werkt niet."""
    station_C_df = aangepaste_gegevens(station_C)
    station_A_df = aangepaste_gegevens(station_A)
    verschillen_dict_C = dict()
    verschillen_dict_A = dict()
    count = 0
    d = 31
    m = 10
    j = 2019
    for bestand in maanden:
        maand = bestand[0:3]
        sneeuwhoogte_C_sat, sneeuwhoogte_A_sat = sneeuwhoogte_sat(bestand, lon, lat)
        sneeuwhoogte_C_stat = station_C_df.Sneeuwhoogte[f"1/{m}/{j}":f"{d}/{m}/{j}"].mean()
        sneeuwhoogte_A_stat = station_A_df.Sneeuwhoogte[f"1/{m}/{j}":f"{d}/{m}/{j}"].mean()
        verschillen_dict_C[maand] = sneeuwhoogte_C_stat - float(sneeuwhoogte_C_sat)
        verschillen_dict_A[maand] = sneeuwhoogte_A_stat - float(sneeuwhoogte_A_sat)
        count +=1
        if count == 1:
            d = 30
            m += 1
        elif count == 2:
            d = 31
            m += 1
        elif count == 3:
            m = "01"
            j = 2020
        elif count == 4:
            d = 29
            m = "02"

    X_as = np.array(5)
    plt.bar(X_as, verschillen_dict_C.values, label = "Courchevel")
    plt.bar(X_as, verschillen_dict_A.values, label ="Alpe de Vénosc")
    plt.legend()
    plt.title("Verschil in sneeuwdiepte tussen het weerstation en de satelliet ")
    plt.show()

def gem_sneeuw_maand (weerstation, maand):
    """Deze functie zoekt de gemiddelde temperatuur van de gegeven maand."""
    maanden_dict = {"jan":1, "feb":2, "maa":3, "apr":4, "mei":5, "jun":6, "jul":7, "aug":8, "sep":9, "okt":10, "nov":11, "dec":12}
    weergegevens_df = aangepaste_gegevens(weerstation)
    maand_getal = maanden_dict[maand[0:3].lower().strip()]
    maand_sneeuw = []
    for index in weergegevens_df.index:
        d, m, j = index.split("/")
        m = int(m)
        if m == maand_getal:
            maand_sneeuw.append(weergegevens_df.loc[index, "Sneeuwhoogte"])   # !!!
    gem_sneeuw = np.nansum(maand_sneeuw)/ len(maand_sneeuw)
    return gem_sneeuw


def verschillen_lijsten (weerstation_1, weerstation_2, lon, lat, sat_geg):
    maanden_lijst = []
    verschillen_lijst_1 = []
    verschillen_lijst_2 = []
    for bestand in sat_geg:
        maanden_lijst.append(bestand[0:3])
        gem_sneeuw_1 = gem_sneeuw_maand(weerstation_1, bestand[0:3])
        gem_sneeuw_2 = gem_sneeuw_maand(weerstation_2, bestand[0:3])
        sneeuw_1, sneeuw_2 = sneeuwhoogte_sat(bestand,lon, lat)
        verschillen_lijst_1.append(gem_sneeuw_1 - sneeuw_1)
        print(f"verschil C: {gem_sneeuw_1 - sneeuw_1}")
        verschillen_lijst_2.append(gem_sneeuw_2 - sneeuw_2)
        print(f"verschil A: {gem_sneeuw_2 - sneeuw_2}")
        print()
    return maanden_lijst, verschillen_lijst_1, verschillen_lijst_2


def verschillen_staafdiagram (weerstation_1, weerstation_2, lon, lat, *sat_geg):
    maanden, lijst_1, lijst_2 = verschillen_lijsten(weerstation_1, weerstation_2, lon, lat, sat_geg)
    x_as = np.arange(len(maanden))
    width = 0.3
    plt.figure(1)
    plt.bar(x_as, lijst_1, width = width, label = "Courchevel")
    plt.bar(x_as + width, lijst_2, width = width, label = "Alpe de Vénosc")
    plt.legend()
    plt.xticks(x_as, maanden)
    plt.xlabel("Maand")
    plt.ylabel("verschil in sneeuwhoogte (m)")
    plt.title("Verschil in sneeuwhoogtes")
    plt.show(block = False)


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
            plt.figure(2)
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

#verschil_staafdiagram_slecht("7893_datums_Courchevel.csv", "7589_datums_L'Alpe_de_Vénosc.csv", "lat.csv", "lon.csv", "okt_Sentinel.csv", "nov_Sentinel.csv", "dec_Sentinel.csv", "jan_Sentinel.csv", "feb_Sentinel.csv")
verschillen_staafdiagram("7893_datums_Courchevel.csv", "7589_datums_L'Alpe_de_Vénosc.csv",  "lon.csv", "lat.csv","okt_Sentinel.csv", "nov_Sentinel.csv", "dec_Sentinel.csv", "jan_Sentinel.csv", "feb_Sentinel.csv")
heatmap_meerdere_maanden()

#inputs:
"""
7893_datums_Courchevel.csv
7589_datums_L'Alpe_de_Vénosc.csv
okt_Sentinel.csv, nov_Sentinel.csv, dec_Sentinel.csv, jan_Sentinel.csv, feb_Sentinel.csv
lat.csv
lon.csv
"""