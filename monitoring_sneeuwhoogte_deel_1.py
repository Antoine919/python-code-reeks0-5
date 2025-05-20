import numpy as np
import pandas as pd
import math


def lezer (locatie):
    """ Laadt de gegevens in als een dataframe en geeft de kolommen een gepaste naam."""
    dataframe = pd.read_csv(locatie, names = ["Datum", "Sneeuwhoogte", "Temperatuur", "Neerslag"], index_col = ["Datum"]) # eerst de kolom een naam geven, dan die als index aanduiden
    return dataframe


def opkuisen (dataframe):
    """Bij de temperatuur wordt een missende waarde aangeduid met 0 K of NaN.
    Zorgt dat alle ontbrekende waarden worden weergegeven met NaN.
    Zet bovendien de temperatuur om naar graden Celsius om de interpretatie te vergemakkelijken.
    Op de dagen dat er geen temperatuur gemeten werd, ontbreken ook de metingen van de neerslag en de sneeuwhoogte. Momenteel staan deze in de dataset aangeduid met
waarde nul (neerslag) of NaN (sneeuwhoogte). Zet al deze waarden om naar NaN. """
    for x in dataframe.index:
        if dataframe.loc[x, "Temperatuur"] == 0 or math.isnan(dataframe.loc[x, "Temperatuur"]): #als de temp NaN is, moet ook de neerslag naar NaN gezet worden
            dataframe.loc[x, "Temperatuur"] = np.nan # en niet = "NaN"
            dataframe.loc[x, "Neerslag"] = np.nan   #alleen als er geen temp gemeten is moet de neerslag NaN zijn, als de neerslag nul is, moet die nul blijven
            dataframe.loc[x, "Sneeuwhoogte"] = np.nan
        else:
            dataframe.loc[x, "Temperatuur"] = dataframe.loc[x, "Temperatuur"] - 273.15
    return dataframe


def aanvullen (dataframe):
    """Maak gebruik van lineaire interpolatie om de missende waarden te schatten. Omdat
vanaf maart het dooiseizoen start en er daarom minder gemeten werd, wordt er slechts tot 1 maart geïnterpoleerd. Maak voor de interpolatie gebruik van de methode
.astype(float).interpolate(method=’linear’). We zijn vanaf nu niet meer geïnteresseerd in
de gegevens vanaf 1 maart. """
   #interpolatie niet in for loop
    #for x in dataframe.index[:"01/03/2020"]:
     #   if dataframe.loc[x, "Temperatuur"] == numpy.nan:
      #      dataframe.loc[x, "Temperatuur"] = dataframe.loc[x, "Temperatuur"].astype(float).interpolate(method = "linear")
       # if dataframe.loc[x, "Neerslag"] == numpy.nan:
        #    dataframe.loc[x, "Neerslag"] = dataframe.loc[x, "Neerslag"].astype(float).interpolate(method = "linear")
       # if dataframe.loc[x, "Sneeuwhoogte"] == numpy.nan:
       #     dataframe.loc[x, "Sneeuwhoogte"] = dataframe.loc[x, "Sneeuwhoogte"].astype(float).interpolate(method = "linear")
    dataframe["Temperatuur"] = dataframe["Temperatuur"].astype(float).interpolate(method = "linear")
    dataframe.Sneeuwhoogte = dataframe.Sneeuwhoogte.astype(float).interpolate(method = "linear")
    dataframe.Neerslag = dataframe.Neerslag.astype(float).interpolate(method = "linear")
    return dataframe.loc[:"29/02/2020"] #er moet nog .loc bij en is inclusief !!


def temp_min (dataframe):
    """Bepaalt op welke dag de laagste temperatuur werd gemeten en bepaalt ook de minimale temperatuur zelf. Print deze resultaten op het scherm."""
    temp_lijst_zonder_NaN = []
    for datum in dataframe.index:
        if not math.isnan(dataframe.loc[datum, "Temperatuur"]):
            temp_lijst_zonder_NaN.append(dataframe.loc[datum, "Temperatuur"])
    laagste_temp = min(temp_lijst_zonder_NaN) #geeft minimum van die kolom, NaN wordt als minimum gezien denk ik, dus eerst opkuisen
    laagste_dag = ""
    for datum in dataframe.index:
        if dataframe.loc[datum, "Temperatuur"] == laagste_temp:
            laagste_dag = datum
    return laagste_dag, "{:.1f}".format(laagste_temp)


def sneeuwdagen (dataframe):
    """Bepaalt op hoeveel dagen er sneeuw viel en bepaalt ook de dag waarop de grootste
hoeveelheid sneeuw viel. Print deze resultaten op het scherm.(Wanneer de temperatuur
minder dan 2 °C bedraagt, valt de neerslag onder de vorm van sneeuw.)"""
    sneeuwdagen_dict = {}
    aantal_sneeuwdagen = 0
    for datum in dataframe.index:
        if dataframe.loc[datum, "Temperatuur"] < 2 and dataframe.loc[datum, "Neerslag"] > 0: # er moet ook als voorwaarde zijn dat er neerslag was, anders valt er geen sneeuw!!
            sneeuwdagen_dict[dataframe.loc[datum, "Neerslag"]] = datum
            aantal_sneeuwdagen += 1
    grootste_neerslag_hoeveelheid = max(sneeuwdagen_dict.keys())
    meeste_sneeuw_datum = sneeuwdagen_dict[grootste_neerslag_hoeveelheid]
    return aantal_sneeuwdagen, grootste_neerslag_hoeveelheid, meeste_sneeuw_datum #aantal sneeuwdagen meten werkt niet met len(sneeuwdagen_dict), wss omdat er dagen zijn met zelfde sneeuwhoeveelheid dus die worden overschreven


def aantal_skidagen (dataframe):
    """Bepaalt het aantal dagen waarop er geskied kon worden. Print dit resultaat op het scherm.
    (De pistes openen enkel wanneer de dikte van de sneeuwlaag minimum 40 cm bedraagt.)"""
    skidagen = 0
    for x in dataframe.index:
        if dataframe.loc[x, "Sneeuwhoogte"] >= 0.40:
            skidagen += 1
    return skidagen


def aangepaste_gegevens (locatie, printen = False):
    """Deze functie maakt een csv-bestand proper en geeft samenvattende info.
    Er is een optionele parameter "printen" met als default waarde "False", als True wordt gegeven, dan wordt een samenvatting van de gegevens geprint."""
    dataframe = lezer(locatie)
    dataframe = opkuisen(dataframe)
    dataframe = aanvullen(dataframe)
    koudste_dag, min_temp = temp_min(dataframe)
    aantal_sneeuwdagen, meeste_sneeuw_hoogte, meeste_sneeuw_datum = sneeuwdagen(dataframe)
    skidagen = aantal_skidagen(dataframe)
    if printen:
        print(f"De koudste dag was {koudste_dag} en de temperatuur bedroeg toen {min_temp}.\n"
               f"Het heeft op {aantal_sneeuwdagen} dagen gesneeuwd en de meeste sneeuw viel op {meeste_sneeuw_datum}, dat was toen {meeste_sneeuw_hoogte} mm.\n"
                f"Er kon op {skidagen} dagen geskied worden.\n")
    return dataframe