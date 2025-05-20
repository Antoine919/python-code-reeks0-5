# vervang de vraagtekens en vul dit script verder aan om de correcte figuur te bekomen

#In het script zal je merken dat de eerste regel code import matplotlib.pyplot as plt is. Het deel as plt is niet noodzakelijk, maar bespaart je wel veel typwerk in de volgende stappen. In plaats van matplotlib.pyplot te gebruiken, kan je immers gewoon plt gebruiken laad de gegevens in vanuit het csv-bestand (klimatologische_gegevens.csv)
#plaats de gegevens in een lijst van lijsten

#zet deze gegevens in 3 lijsten: maanden, temperatuur en neerslag
#maanden =
#temperatuur =
#neerslag =

#plot de gegevens uit deze lijsten


import matplotlib.pyplot as plt
import csv


maanden = []
temperatuur = []
neerslag = []
#zie oplossing voor alternatief: eerst een lijst maken van reader_obj: dataset = list(reader_obj)
with open("klimatologische_gegevens.csv", "r") as bestand:
    lezer_obj = csv.reader(bestand)
    for regel in lezer_obj: #Hoe begin je te lezen vanaf een bepaalde regel, niet van begin? ==> onder lezer_obj = ... next(lezer_obj), slaat eerste regel over
        try:
            maanden.append((regel[0]))
            temperatuur.append(float(regel[1]))
            neerslag.append(float(regel[2]))
        except ValueError:
            temperatuur.append(regel[1])
            neerslag.append(regel[2])
    maanden.remove("maanden")
    temperatuur.remove("temperatuur")
    neerslag.remove("neerslag")


plt.figure(1)
plt.plot(maanden, temperatuur)
plt.title("Temperatuur in Brussel per maand")
plt.xlabel("Maand")
plt.ylabel("Temperatuur (°C)")

plt.figure(2)
plt.bar(maanden, neerslag)
plt.title("Neerslag in Brussel per maand")
plt.xlabel("Maand")
plt.ylabel("Neerslag (mm)")
plt.ylim(0,100)

plt.show()
