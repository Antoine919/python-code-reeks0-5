import matplotlib.pyplot as plt
from monitoring_sneeuwhoogte_deel_1 import aangepaste_gegevens

def plots_mooi (gebied_1, bestand_1, gebied_2, bestand_2):
    """ Deze functie maakt samenvattende plots van 2 skigebieden. Het voortschrijdende gemiddelde is wekelijks.
    De figuren worden tevens als PDF opgeslagen. Maar in plaats van plt.plot te gebruiken, wordt de nieuwe gekuiste dataframe direct geplot, zo komen de data mooi op de assen te staan en niet op elkaar gepropt.
    Er wordt eerste een nieuwe kolommen aan het dataframe toegevoegd met de rolling mean."""

    print(gebied_1, ":")
    dataframe_1 = aangepaste_gegevens(bestand_1, printen = True)
    dataframe_1["gem_temp"] = dataframe_1.Temperatuur.rolling(7).mean()
    dataframe_1["gem_sneeuwhoogte"] = dataframe_1.Sneeuwhoogte.rolling(7).mean()
    print(gebied_2, ":")
    dataframe_2 = aangepaste_gegevens(bestand_2, printen = True)
    dataframe_2["gem_temp"] = dataframe_2.Temperatuur.rolling(7).mean()
    dataframe_2["gem_sneeuwhoogte"] = dataframe_2.Sneeuwhoogte.rolling(7).mean()

    # temperatuur plots:

    #subplots maken lukt ons niet, miss kan het, maar geen idee hoe


    fig_1_gebied_1 = dataframe_1.plot(y = "Temperatuur", use_index = "True", label = gebied_1)  #use_index = "True" is de enige manier om de index kolom als x-waardes te kunnen gebruiken
    dataframe_2.plot(ax = fig_1_gebied_1, y = "Temperatuur", use_index = "True", label = gebied_2)
    plt.axhline(2, label = "Sneeuwgrens", color = "red")
    plt.legend()
    plt.xlabel("Datum")
    plt.ylabel("Temperatuur (°C)")
    plt.title("Temperatuur in functie van de tijd", color = "Blue")
    plt.savefig("monitoring_sneeuwhoogte_temp_plot_mooipdf")


    fig_2_gebied1 = dataframe_1.plot(y = "gem_temp", use_index = "True", label = gebied_1)
    dataframe_2.plot(ax = fig_2_gebied1, y = "gem_temp", use_index = "True", label = gebied_2)
    plt.axhline(2, label = "Sneeuwgrens", color = "red")
    plt.legend()
    plt.xlabel("Datum")
    plt.ylabel("voortschrijdende gemiddelde temperatuur (°C)")
    plt.title("Voortschrijdend gemiddelde temperatuur in functie van de tijd")


    plt.savefig("monitoring_sneeuwhoogte_rolling_mean_temp_plot_mooi.pdf")

    # sneeuwhoogte plot

    plt.figure(2)
    fig_3_gebied_1 = dataframe_1.plot(y = "gem_sneeuwhoogte", use_index = True, label = gebied_1)
    dataframe_2.plot(ax = fig_3_gebied_1, y = "gem_sneeuwhoogte", use_index = True, label=gebied_2)
    plt.axhline(0.40, label = "Skigrens", color = "red")
    plt.legend()
    plt.xlabel("Datum")
    plt.ylabel("Voortschrijdend gemiddelde sneeuwhoogte (m)")
    plt.title("Voortschrijdend gemiddelde sneeuwhoogte i.f.v. de tijd")
    plt.savefig("monitoring_sneeuwhoogte_sneeuwhoogte_plot_mooi.pdf")

    return plt.show()

