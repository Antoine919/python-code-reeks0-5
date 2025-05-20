# * importeert alles van dat programma, runt het ook eerst volledig, dus best alleen functies in dat bestand steken
from dna_functies_deel_1_2_3 import *


locatie_seq = input("Geef de locatie van je .txt bestand met de dna sequentie: ")
locatie_codon_tabel = input("Geef de locatie van je csv bestand met de codontabel: ")
locatie_oplossing = input("Geef de locatie van je .txt bestand met de oplossing: ")
print()
print(dna_translatie_deel_1_2_3(locatie_seq, locatie_codon_tabel, locatie_oplossing))


#inputs:
"""
dna.txt
aacodons_table.csv
AZ_keten_oplossing.txt
"""