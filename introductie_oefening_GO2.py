import pandas as pd
import matplotlib.pyplot as plt


dataframe = pd.read_csv("klimatologische_gegevens.csv", index_col= ["maanden"])

"""
print(dataframe)
print()
dataframe.info()
print()
print(dataframe.shape)
print()
print(dataframe.loc["jan"])
print()
print(dataframe.loc[["jan","aug"]]) #eerst index van de rij dan kolom
print()
print(dataframe.loc["jan", "temperatuur"])
print()
print(dataframe.temperatuur)
#Het datatype dat je verkrijgt is een Pandas Series en kan je zien als een kolom van een tabel (eendimensionaal).
print()
print(dataframe["temperatuur"]) 
print()
print(dataframe["temperatuur"][1]) #gaat binnenkort niet meer mogen in nieuwe update, best .loc gebruiken
print()
print(dataframe['temperatuur']['feb'])
print()
print(dataframe.index)
print()
dataframe['maand']=[1,2,3,4,5,6,7,8,9,10,11,12]
print()
print(dataframe)
print()
del dataframe['maand']
print()
print(dataframe)
"""


plt.subplot(1,2,1)
plt.plot(dataframe.index,dataframe.temperatuur) # je mag niet .maanden, want gebruikt als index, moet .index
plt.title("Temperatuur per maand")
plt.xlabel("Maanden")
plt.ylabel("Temperatuur (°C)")

plt.subplot(1,2,2)
plt.bar(dataframe.index, dataframe.neerslag)
plt.title("Neerslag per maand")
plt.xlabel("Maanden")
plt.ylabel("Neerslag (mm)")
plt.show()