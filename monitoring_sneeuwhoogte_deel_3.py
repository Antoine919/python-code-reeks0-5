# om lijst van lijst te maken is csv makkelijker
import csv
import pandas as pd
import seaborn as sns # seaborn heeft matplotlib pyplot nodig
import matplotlib.pyplot as plt
from Gevorderde_programmeeropdracht_2.monitoring_sneeuwhoogte_deel_1 import aangepaste_gegevens


def lijsten_maken (lengtegraden_csv, breedtegraden_csv, bestand = None):
    """Deze functie maakt lijsten van de ingegeven csv-bestanden."""
    if bestand is not None:
        with open(bestand) as sat_geg:
            lijst_van_lijsten = list(csv.reader(sat_geg))

    with open(lengtegraden_csv) as lengtegraden:
        lengte_reader = csv.reader(lengtegraden)
        lengte_lijst = []
        for regel in lengte_reader:  # ervoor zorgen dat het niet een lijst in een lijst is
            for element in regel:
                lengte_lijst.append(element)


    with open(breedtegraden_csv) as breedtegraden:
        breedte_reader = list(csv.reader(breedtegraden))
        breedte_lijst = []
        for regel in breedte_reader:
            for element in regel:
                breedte_lijst.append(element)
    if bestand is not None:
        return lengte_lijst, breedte_lijst, lijst_van_lijsten
    else:
        return lengte_lijst, breedte_lijst

# het is best om 1 functie te maken die coördinaten zoekt en de echte coord ook als argument te geven, als input
def coord_alpe(lengtegraden_csv, breedtegraden_csv):
    """Bepaalt welke OL en NB (en de bijhorende index) uit de gegeven csv-bestanden er het dichtst bij de coördinaten van het skigebied L’Alpe de Vénosc (44,9467 NB en 6,1883 OL) liggen. """
    lengte_lijst, breedte_lijst = lijsten_maken(lengtegraden_csv, breedtegraden_csv)
    OL = 6.1883
    NB = 44.9467

    index = 0   # bij while initiëren en zelf stap geven
    while index < len(lengte_lijst)-1: # alleen < want index begint bij nul, lijst van lengte 10, index gaat tot 9 en - 1 want ik neem ze per 2
        a = float(lengte_lijst[index])
        b = float(lengte_lijst[index + 1])
        if a <= OL <= b:
            if abs(a - OL) < abs(b - OL):   #absolute waarde niet vergeten!!
                ind_OL = index
                OL_sat = a
            else:
                ind_OL = index + 1
                OL_sat = b
        index += 1

    index = 0
    while index < len(breedte_lijst)-1: # bij deze lijst staat elk element ook nog in een lijst
        c = float(breedte_lijst[index])
        d = float(breedte_lijst[index + 1])
        if c >= NB >= d: # ze staan van groot naar klein
            if abs(c - NB) < abs(d - NB):
                ind_NB = index
                NB_sat = c
            else:
                ind_NB = index + 1
                NB_sat = d
        index += 1
    return ind_NB, NB_sat, ind_OL, OL_sat


def coord_courchevel(lengtegraden_csv, breedtegraden_csv):
    """Bepaalt welke OL en NB (en de bijhorende index) uit de gegeven csv-bestanden er het dichtst bij de coördinaten van het skigebied Courchevel (45,4133 NB en 6,6322 OL) liggen. """
    lengte_lijst, breedte_lijst = lijsten_maken(lengtegraden_csv, breedtegraden_csv)
    OL = 6.6322
    NB = 45.4133

    index = 0   # bij while initiëren en zelf stap geven
    while index < len(lengte_lijst)-1: # alleen < want index begint bij nul, lijst van lengte 10, index gaat tot 9 en - 1 want ik neem ze per 2
        a = float(lengte_lijst[index])
        b = float(lengte_lijst[index + 1])
        if a <= OL <= b:
            if abs(a - OL) < abs(b - OL):   #absolute waarde niet vergeten!!
                ind_OL = index
                OL_sat = a
            else:
                ind_OL = index + 1
                OL_sat = b
        index += 1

    index = 0
    while index < len(breedte_lijst)-1:
        c = float(breedte_lijst[index])
        d = float(breedte_lijst[index + 1])
        if c >= NB >= d: # ze staan van groot naar klein
            if abs(c - NB) < abs(d - NB):
                ind_NB = index
                NB_sat = c
            else:
                ind_NB = index + 1
                NB_sat = d
        index += 1
    return ind_NB, NB_sat, ind_OL, OL_sat


def sneeuwhoogte_sat (sat_geg, lengtegraden_csv, breedtegraden_csv):
    """Deze functie extraheert de sneeuwdiepte van station 7589 in het skigebied L’Alpe de Vénosc en
station 7893 voor Courchevel voor de maand januari a.d.h.v. de gegeven csv-bestanden. Gebruikt de dichtstbijzijnde OL en NB."""
    lijst_van_lijsten = lijsten_maken(lengtegraden_csv, breedtegraden_csv, sat_geg)[2]
    ind_NB_C, NB_sat_C, ind_OL_C, OL_sat_C = coord_courchevel(lengtegraden_csv, breedtegraden_csv)
    sneeuwhoogte_C = lijst_van_lijsten[ind_NB_C][ind_OL_C]
    ind_NB_A, NB_sat_A, ind_OL_A, OL_sat_A = coord_alpe(lengtegraden_csv, breedtegraden_csv)
    sneeuwhoogte_A = lijst_van_lijsten[ind_NB_A][ind_OL_A]
    return float(sneeuwhoogte_C), float(sneeuwhoogte_A)


def gem_sneeuw_januari_weerstat (stat_bestand_1, stat_bestand_2):
    """Deze functie geeft de gemiddelde temperatuur van de maand januari uit 2 stations. Deze wordt gehaald uit een csv-bestand met gegevens van 2 weerstations. De gegevens worden ook eerst gekuist voor gebruik."""
    dataframe_1 = aangepaste_gegevens(stat_bestand_1)
    dataframe_2 = aangepaste_gegevens(stat_bestand_2)
    gem_sneeuw_station_1 = dataframe_1.Sneeuwhoogte["1/01/2020":"31/01/2020"].mean()
    gem_sneeuw_station_2 = dataframe_2.Sneeuwhoogte["1/01/2020":"31/01/2020"].mean()
    return float(gem_sneeuw_station_1), float(gem_sneeuw_station_2)

def heatmap (sat_geg, lengtegraden_csv, breedtegraden_csv):
    """Deze functie maakt een heatmap van de sneeuwhoogte a.d.h.v. 3 csv-bestanden: een bestand met satelliet gegevens over de sneeuwhoogte, een bestand met de lengtegraden, en 1 met de breedtegraden."""
    lengte_lijst, breedte_lijst = lijsten_maken(lengtegraden_csv, breedtegraden_csv)
    frame_sneeuw = pd.read_csv(sat_geg, names = lengte_lijst) # de lengtegraden als hoofding zetten zodat ze op de x-as komen van de heatmap en zodat de eerste rij gegevens niet verloren gaat
    frame_sneeuw.index = breedte_lijst # de indices vervangen door de breedtegraden om op y-as te zetten
    sns.heatmap(frame_sneeuw, cmap = "mako") # icefire of coolwarm kan ook, standaard is rocket
    plt.xlabel("oosterlengte (°)")
    plt.ylabel("noorderbreedte (°)")
    plt.title("Sneeuwkaart Alpengebied")
    plt.savefig("Heatmap_sneeuwhoogte_januari_alpengebied.pdf")
    return plt.show()


# tests
"""
print(coord_alpe("lon.csv", "lat.csv"))
print()
print(coord_courchevel("lon.csv", "lat.csv"))
print()
print(sneeuwhoogte_sat("jan_Sentinel.csv", "lon.csv", "lat.csv",))
print()
print(gem_sneeuw_januari_weerstat("7893_datums_Courchevel.csv","7589_datums_L'Alpe_de_Vénosc.csv"))
heatmap("jan_Sentinel.csv", "lon.csv", "lat.csv")
"""