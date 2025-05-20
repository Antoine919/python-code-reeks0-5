import csv


def string_omzetting_veilig (locatie):
    """Deze functie zet een .txt bestand om naar één regel (datatype string), waarbij alles in hoofdletters wordt omgezet.
    Als het gegeven bestand niet gevonden wordt, vraagt de functie een nieuw bestand. """
    dna_seq = ""
    # hoeft niet met blijven_gaan = True en while blijven_gaan is True
    # is een oneindige loop waaruit je breekt als je het juist bestand hebt
    while True:
        try:
            with open(locatie, "r") as dna_seq_txt:
                for regel in dna_seq_txt:
                    regel = regel.strip("\n")
                    dna_seq += regel.upper()
            return dna_seq
        except FileNotFoundError:
            print("Het opgegeven bestand met de dna streng werd niet gevonden, geef een nieuw bestand in:")
            locatie = input()



def string_omzetting_minder_veilig (locatie):
    """Deze functie zet een .txt bestand om naar één regel (datatype string), waarbij alles in hoofdletters wordt omgezet. """
    dna_seq = ""
    try:
        with open(locatie, "r") as dna_seq_txt:
            for regel in dna_seq_txt:
                regel = regel.strip("\n")
                dna_seq += regel.upper()
    except FileNotFoundError:
        print("Het opgegeven bestand werd niet gevonden, geef een nieuw bestand in:")
        locatie = input()
        dna_seq = string_omzetting_minder_veilig(locatie)
    return dna_seq


def find_startcodon_deel_1_2_3 (dna_seq_string):
    """Deze functie neemt een dna sequentie, met als datatype string, en geeft de index van de eerste base van het eerste startcodon terug als integer.
    Als de sequentie geen startcodon bevat, wordt dit gemeld en stopt het programma."""
    index_startcodon = 0
    # als je een slice neemt, kan je geen IndexError krijgen, alleen als je 1 element eruit haalt
    while dna_seq_string[index_startcodon:index_startcodon + 3] != "ATG":
        codon = dna_seq_string[index_startcodon:index_startcodon + 3]
        index_startcodon += 1 # hier stap van 1 om binnen alle frames te kijken (springen van eerste, naar tweede, naar derde) om de eerst voorkomende startcodon te vinden
        if len(codon) != 3:
            print("De dna sequentie bevat geen startcodon.")
            exit()
    return int(index_startcodon)


def codon_omzetting_while (dna_seq):
    """Deze functie neemt een dna_seq (string) en maakt een lijst met alle codons, startend vanaf het eerste startcodon en stopt bij het eerste stopcodon (en zet het stopcodon niet in de lijst).
    Als de sequentie geen stopcodon bevat, wordt dit gemeld en gebeurt de omzetting tot het einde van de gegeven sequentie. """
    codon_lijst = []
    index = find_startcodon_deel_1_2_3(dna_seq)
    # while dna_seq[index:index + 3] != "TAA" or "TGA" or "TAG": als meerdere opties in tuple
    while dna_seq[index:index + 3] not in ("TAA", "TGA", "TAG"):
        if len(dna_seq[index: index + 3]) != 3:
            print("De sequentie bevat geen stopcodon.")
            return codon_lijst
        codon_lijst.append(dna_seq[index: index + 3])
        index += 3
    return codon_lijst


def codon_omzetting_for (dna_seq):
    """Deze functie neemt een dna_seq (string) en maakt een lijst met alle codons, startend vanaf het eerste startcodon en stopt bij het eerste stopcodon (en zet het stopcodon niet in de lijst).
     Als de sequentie geen stopcodon bevat, wordt dit gemeld en gebeurt de omzetting tot het einde van de gegeven sequentie."""
    codon_lijst = []
    index = find_startcodon_deel_1_2_3(dna_seq)
    # while dna_seq[index:index + 3] != "TAA" or "TGA" or "TAG": als meerdere opties in tuple
    for index in range(index, len(dna_seq), 3):
        if dna_seq[index: index + 3] in ("TAA", "TGA", "TAG"):
            break
        if len(dna_seq[index: index + 3]) != 3:
            print("De sequentie bevat geen stopcodon.")
            break
        codon_lijst.append(dna_seq[index: index + 3])
    return codon_lijst


def csv_to_dict (locatie):
    """Deze functie zet een csv-bestand met codons en de gecodeerde aminozuren in een dictionary met de codon als key en het gecodeerde AZ als value.
    Als het gegeven bestand niet gevonden wordt, vraagt de functie een nieuw bestand."""
    AZ_dict = dict()
    while True:
        try:
            with open(locatie, "r") as csv_bestand:
                reader_object = csv.reader(csv_bestand)
                for regel in reader_object:
                    AZ_dict[regel[0]] = regel[2]
            return AZ_dict
        except FileNotFoundError:
            print("Het opgegeven bestand met de codon tabel werd niet gevonden, geef een nieuw bestand in:")
            locatie = input()


def seq_naar_AZ_keten (codon_lijst, AZ_dict):
    """Deze functie zet een dna sequentie om naar een aminozuurketen (datatype string)."""
    AZ_keten=""
    for codon in codon_lijst:
        AZ_keten += AZ_dict[codon]
    return AZ_keten


def controle (AZ_keten, locatie_oplossing):
    """Deze functie checkt of een opgegeven AZ-keten (datatype string) overeenkomt met de AZ-keten die in het opgegeven .txt bestand staat.
    Als het gegeven bestand niet gevonden wordt, vraagt de functie een nieuw bestand."""
    while True:
        try:
            with open(locatie_oplossing, "r") as oplossing:
                AZ_keten_juist = oplossing.read()
            if AZ_keten_juist == AZ_keten:
                return True
            else:
                return False
        except FileNotFoundError:
            print("Het opgegeven bestand met de oplossing werd niet gevonden, geef een nieuw bestand in:")
            locatie_oplossing = input()


def complementaire_streng (dna_seq):
    """Deze functie geeft de complementaire streng (type string) terug van een ingegeven dna streng (type string)."""
    comp_seq = ""
    base_dict = {"A": "T", "T": "A", "G": "C", "C": "G"}
    for base in dna_seq:
        comp_seq += base_dict[base]
    return comp_seq


def dna_translatie_deel_1_2_3 (locatie_seq, locatie_codon_tabel,locatie_oplossing):
    """Deze functie zet een dna sequentie die in een .txt bestand staat om in een aminozuursequentie. Hiervoor gebruikt de functie het opgegeven csv-bestand met de codon-tabel. Achteraf checkt de functie of de gevonden AZ-keten overeenkomt met de keten in het oplossingsbestand (.txt)."""
    dna_seq = string_omzetting_veilig(locatie_seq)
    codon_lijst = codon_omzetting_while(dna_seq)
    AZ_dict = csv_to_dict(locatie_codon_tabel)
    AZ_keten = seq_naar_AZ_keten(codon_lijst, AZ_dict)
    controle_string = controle(AZ_keten, locatie_oplossing)
    return AZ_keten + "\n" + str(controle_string)


#tests:
"""
dna_seq = string_omzetting_veilig("dna.txp")
index = find_startcodon_deel_1_2_3(dna_seq)
codon_lijst = codon_omzetting_while(dna_seq)
codon_lijst_2 = codon_omzetting_for(dna_seq)
AZ_dict = csv_to_dict("aacodons_table.csv")
AZ_keten = seq_naar_AZ_keten(codon_lijst, AZ_dict)
print(dna_seq)
print(index)
print(dna_seq.find("ATG"))
print(codon_lijst)
print(codon_lijst_2)
print(AZ_dict)
print(AZ_keten)
print(controle(AZ_keten, "AZ_keten_oplossing.txt"))
print()
print(complementaire_streng(dna_seq))
print()
print(codon_omzetting_while("ATGJHGK"))
print(codon_omzetting_for("ATGJHGK"))
index = find_startcodon_deel_1_2_3("ABSDEJ")
print(index)
"""