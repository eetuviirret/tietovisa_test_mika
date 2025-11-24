import random
import mysql.connector
import tarina
from geopy import distance

#SQL yhteys
yhteys = mysql.connector.connect(
    host='localhost',
    port=3307, #3306 jos sinne asennettu MySQL
    database='flight_game',
    user='root',
    password='mikasana', #KÄYTTÄJÄN SALASANA
    autocommit=True
)

#Vastausvalikko -funktio, joka printtaa kysymyksen ja vastausvaihtoehdot
def vastausvalikko(kysymys_sanakirja):
    if kysymys_sanakirja["kysymysteksti"][0] == "What is the distance between " or kysymys_sanakirja["kysymysteksti"][0] == "How many kilotons of CO2 emmission are produced on a flight between ":
        print(
            f"{kysymys_sanakirja['kysymysteksti'][0]}{kysymys_sanakirja['kysymys'][0][0]} and {kysymys_sanakirja['kysymys'][1][0]}{kysymys_sanakirja['kysymysteksti'][1]}")
        print(f"{kysymys_sanakirja['vastaus1'][0]}. {kysymys_sanakirja['vastaus1'][1]}")
        print(f"{kysymys_sanakirja['vastaus2'][0]}. {kysymys_sanakirja['vastaus2'][1]}")
        print(f"{kysymys_sanakirja['vastaus3'][0]}. {kysymys_sanakirja['vastaus3'][1]}")
        print(f"{kysymys_sanakirja['vastaus4'][0]}. {kysymys_sanakirja['vastaus4'][1]}")
    else:
        print(
            f"{kysymys_sanakirja['kysymysteksti'][0]}{kysymys_sanakirja['kysymys'][0]}{kysymys_sanakirja['kysymysteksti'][1]}")
        print(f"{kysymys_sanakirja['vastaus1'][0]}. {kysymys_sanakirja['vastaus1'][1]}")
        print(f"{kysymys_sanakirja['vastaus2'][0]}. {kysymys_sanakirja['vastaus2'][1]}")
        print(f"{kysymys_sanakirja['vastaus3'][0]}. {kysymys_sanakirja['vastaus3'][1]}")
        print(f"{kysymys_sanakirja['vastaus4'][0]}. {kysymys_sanakirja['vastaus4'][1]}")

#Kysymys -funktio, joka asettaa sanakirjaan kysymyksen ja vastaukset
def kysymysfunktio(i):
    # Sanakirja, johon vastaukset talletetaan
    vastauslista = {}

    # Lista joka asettaa oikeat ja väärät vastaukset satunnaiseen järjestykseen
    random_lista = ["1", "2", "3", "4"]
    random.shuffle(random_lista)

    #Jos kierrosnumero on alle 6, valitaan kysymys helpoista kysymyksistä
    if i < 6:
        #Luodaan helppo kysymys, valitaan 1 eri kysymyksistä
        kysymysvalinta = random.randint(1, 4)

        #KYSYMYS: MISSÄ LENTOKENTTÄ SIJAITSEE (EU/US)
        if kysymysvalinta == 1:
            question_text = ["What country is ", " located in?"]
            #Haetaan kysymykseen muuttuja
            sql = f"SELECT name, ident FROM airport WHERE continent = 'EU' OR continent = 'US' ORDER BY RAND() LIMIT 1"
            kursori = yhteys.cursor()
            kursori.execute(sql)
            #Haun tulos muuttujaan
            kysymys = kursori.fetchone()

            #Haetaan kysymykseen vastaus
            sql = f"SELECT name, iso_country FROM country WHERE iso_country in(SELECT iso_country FROM airport WHERE ident = '{kysymys[1]}')"
            kursori = yhteys.cursor()
            kursori.execute(sql)
            #Oikea vastaus muuttujaan
            oikea_vastaus = kursori.fetchone()

            #Haetaan 3 väärää vastausta
            sql = f"SELECT name FROM country WHERE NOT iso_country = '{oikea_vastaus[1]}' ORDER BY RAND() LIMIT 3"
            kursori = yhteys.cursor()
            kursori.execute(sql)
            #Väärät vastaukset muuttujaan
            vaarat_vastaukset = kursori.fetchall()

            #Luodaan vastauslista, jossa vastauksen järjestys määräytyy random_listan mukaan
            vastauslista[f"vastaus{random_lista[0]}"] = oikea_vastaus[0], 1
            vastauslista[f"vastaus{random_lista[1]}"] = vaarat_vastaukset[0][0], 0
            vastauslista[f"vastaus{random_lista[2]}"] = vaarat_vastaukset[1][0], 0
            vastauslista[f"vastaus{random_lista[3]}"] = vaarat_vastaukset[2][0], 0

        #KYSYMYS: MITEN KORKEALLA LENTOKENTTÄ SIJAITSEE (EU/US)
        elif kysymysvalinta == 2:
            question_text = ["What is the elevation of ", " airport in meters?"]
            # Haetaan kysymykseen muuttuja
            sql = f"SELECT name, ident FROM airport WHERE continent = 'EU' OR continent = 'US' ORDER BY RAND() LIMIT 1"
            kursori = yhteys.cursor()
            kursori.execute(sql)
            # Haun tulos muuttujaan
            kysymys = kursori.fetchone()

            sql = f"SELECT elevation_ft*0.3048 as elevation_m FROM airport WHERE ident = '{kysymys[1]}'"
            kursori = yhteys.cursor()
            kursori.execute(sql)
            # Oikea vastaus muuttujaan
            oikea_vastaus = kursori.fetchone()

            # Haetaan 3 väärää vastausta
            sql = f"SELECT DISTINCT elevation_ft*0.3048 as elevation_m FROM airport WHERE NOT ident = '{kysymys[1]}' AND NOT elevation_ft*0.3048 = {oikea_vastaus[0]} ORDER BY RAND() LIMIT 3"
            kursori = yhteys.cursor()
            kursori.execute(sql)
            # Väärät vastaukset muuttujaan
            vaarat_vastaukset = kursori.fetchall()

            # Luodaan vastauslista, jossa vastauksen järjestys määräytyy random_listan mukaan
            vastauslista[f"vastaus{random_lista[0]}"] = oikea_vastaus[0], 1
            vastauslista[f"vastaus{random_lista[1]}"] = vaarat_vastaukset[0][0], 0
            vastauslista[f"vastaus{random_lista[2]}"] = vaarat_vastaukset[1][0], 0
            vastauslista[f"vastaus{random_lista[3]}"] = vaarat_vastaukset[2][0], 0

        # KYSYMYS: LENTOKENTTIEN VÄLINEN ETÄISYYS (EU)
        elif kysymysvalinta == 3:
            question_text = ["What is the distance between ", " airports in kilometers?"]
            # Haetaan kysymykseen muuttujat
            sql = f"SELECT name, ident, latitude_deg, longitude_deg FROM airport WHERE continent = 'EU' ORDER BY RAND() LIMIT 2"
            kursori = yhteys.cursor()
            kursori.execute(sql)
            kysymys = kursori.fetchall()

            # Lasketaan kahden haetun lentokentän etäisyys
            start = [kysymys[0][2], kysymys[0][3]]
            end = [kysymys[1][2], kysymys[1][3]]

            # Oikea vastaus palautetaan kokonaislukuna
            oikea_vastaus = [int(distance.distance((start[0], start[1]), (end[0], end[1])).km)]

            # Luodaan random luvut vääriksi vastauksiksi
            vaarat_vastaukset = [random.randint(0, 10000), random.randint(0, 10000), random.randint(0, 10000)]

            # Luodaan vastauslista, jossa vastauksen järjestys määräytyy random_listan mukaan
            vastauslista[f"vastaus{random_lista[0]}"] = oikea_vastaus[0], 1
            vastauslista[f"vastaus{random_lista[1]}"] = vaarat_vastaukset[0], 0
            vastauslista[f"vastaus{random_lista[2]}"] = vaarat_vastaukset[1], 0
            vastauslista[f"vastaus{random_lista[3]}"] = vaarat_vastaukset[2], 0

        #KYSYMYS: MIKÄ LENTOKENTTÄ ON KORKEIN
        elif kysymysvalinta == 4:
            question_text = ["Which airport has the elevation of ", " meters from the sea surface?"]
            # Haetaan kysymykseen muuttuja
            sql = f"SELECT elevation_ft*0.3048 as elevation_m, ident FROM airport ORDER BY RAND() LIMIT 1"
            kursori = yhteys.cursor()
            kursori.execute(sql)
            # Haun tulos muuttujaan
            kysymys = kursori.fetchone()

            sql = f"SELECT name FROM airport WHERE ident = '{kysymys[1]}'"
            kursori = yhteys.cursor()
            kursori.execute(sql)
            # Oikea vastaus muuttujaan
            oikea_vastaus = kursori.fetchone()

            # Haetaan 3 väärää vastausta
            sql = f"SELECT DISTINCT name FROM airport WHERE NOT ident = '{kysymys[1]}' AND NOT elevation_ft*0.3048 = {kysymys[0]} ORDER BY RAND() LIMIT 3"
            kursori = yhteys.cursor()
            kursori.execute(sql)
            # Väärät vastaukset muuttujaan
            vaarat_vastaukset = kursori.fetchall()

            # Luodaan vastauslista, jossa vastauksen järjestys määräytyy random_listan mukaan
            vastauslista[f"vastaus{random_lista[0]}"] = oikea_vastaus[0], 1
            vastauslista[f"vastaus{random_lista[1]}"] = vaarat_vastaukset[0][0], 0
            vastauslista[f"vastaus{random_lista[2]}"] = vaarat_vastaukset[1][0], 0
            vastauslista[f"vastaus{random_lista[3]}"] = vaarat_vastaukset[2][0], 0

    #Jos kierrosnumero on alle 11, valitaan kysymys keskivaikeista kysymyksistä
    elif i < 11:
        #Luodaan keskivaikea kysymys
        kysymysvalinta = random.randint(1, 4)

        #KYSYMYS: MIKÄ ON LENTOKENTÄN ICAO -KOODI
        if kysymysvalinta == 1:
            question_text = ["What is the ICAO -code of ", "?"]
            # Haetaan kysymykseen muuttuja
            sql = f"SELECT name, ident FROM airport ORDER BY RAND() LIMIT 1"
            kursori = yhteys.cursor()
            kursori.execute(sql)
            # Haun tulos muuttujaan
            kysymys = kursori.fetchone()

            # Haetaan kysymykseen vastaus
            sql = f"SELECT ident FROM airport WHERE ident = '{kysymys[1]}'"
            kursori = yhteys.cursor()
            kursori.execute(sql)
            # Oikea vastaus muuttujaan
            oikea_vastaus = kursori.fetchone()

            # Haetaan 3 väärää vastausta
            sql = f"SELECT ident FROM airport WHERE NOT ident = '{oikea_vastaus[0]}' ORDER BY RAND() LIMIT 3"
            kursori = yhteys.cursor()
            kursori.execute(sql)
            # Väärät vastaukset muuttujaan
            vaarat_vastaukset = kursori.fetchall()

            # Luodaan vastauslista, jossa vastauksen järjestys määräytyy random_listan mukaan
            vastauslista[f"vastaus{random_lista[0]}"] = oikea_vastaus[0], 1
            vastauslista[f"vastaus{random_lista[1]}"] = vaarat_vastaukset[0][0], 0
            vastauslista[f"vastaus{random_lista[2]}"] = vaarat_vastaukset[1][0], 0
            vastauslista[f"vastaus{random_lista[3]}"] = vaarat_vastaukset[2][0], 0

        # KYSYMYS: MISSÄ LENTOKENTTÄ SIJAITSEE (AU/SA)
        elif kysymysvalinta == 2:
            question_text = ["What country is ", " located in?"]
            # Haetaan kysymykseen muuttuja
            sql = f"SELECT name, ident FROM airport WHERE continent = 'AU' OR continent = 'SA' ORDER BY RAND() LIMIT 1"
            kursori = yhteys.cursor()
            kursori.execute(sql)
            # Haun tulos muuttujaan
            kysymys = kursori.fetchone()

            # Haetaan kysymykseen vastaus
            sql = f"SELECT name, iso_country FROM country WHERE iso_country in(SELECT iso_country FROM airport WHERE ident = '{kysymys[1]}')"
            kursori = yhteys.cursor()
            kursori.execute(sql)
            # Oikea vastaus muuttujaan
            oikea_vastaus = kursori.fetchone()

            # Haetaan 3 väärää vastausta
            sql = f"SELECT name FROM country WHERE NOT iso_country = '{oikea_vastaus[1]}' ORDER BY RAND() LIMIT 3"
            kursori = yhteys.cursor()
            kursori.execute(sql)
            # Väärät vastaukset muuttujaan
            vaarat_vastaukset = kursori.fetchall()

            # Luodaan vastauslista, jossa vastauksen järjestys määräytyy random_listan mukaan
            vastauslista[f"vastaus{random_lista[0]}"] = oikea_vastaus[0], 1
            vastauslista[f"vastaus{random_lista[1]}"] = vaarat_vastaukset[0][0], 0
            vastauslista[f"vastaus{random_lista[2]}"] = vaarat_vastaukset[1][0], 0
            vastauslista[f"vastaus{random_lista[3]}"] = vaarat_vastaukset[2][0], 0

        #KYSYMYS: MITEN KORKEALLA LENTOKENTTÄ SIJAITSEE (SA/AU)
        elif kysymysvalinta == 3:
            question_text = ["What is the elevation of ", " airport in meters?"]
            # Haetaan kysymykseen muuttuja
            sql = f"SELECT name, ident FROM airport WHERE continent = 'SA' OR continent = 'AU' ORDER BY RAND() LIMIT 1"
            kursori = yhteys.cursor()
            kursori.execute(sql)
            # Haun tulos muuttujaan
            kysymys = kursori.fetchone()

            sql = f"SELECT elevation_ft*0.3048 as elevation_m FROM airport WHERE ident = '{kysymys[1]}'"
            kursori = yhteys.cursor()
            kursori.execute(sql)
            # Oikea vastaus muuttujaan
            oikea_vastaus = kursori.fetchone()

            # Haetaan 3 väärää vastausta
            sql = f"SELECT DISTINCT elevation_ft*0.3048 as elevation_m FROM airport WHERE NOT ident = '{kysymys[1]}'AND NOT elevation_ft*0.3048 = {oikea_vastaus[0]} ORDER BY RAND() LIMIT 3"
            kursori = yhteys.cursor()
            kursori.execute(sql)
            # Väärät vastaukset muuttujaan
            vaarat_vastaukset = kursori.fetchall()

            # Luodaan vastauslista, jossa vastauksen järjestys määräytyy random_listan mukaan
            vastauslista[f"vastaus{random_lista[0]}"] = oikea_vastaus[0], 1
            vastauslista[f"vastaus{random_lista[1]}"] = vaarat_vastaukset[0][0], 0
            vastauslista[f"vastaus{random_lista[2]}"] = vaarat_vastaukset[1][0], 0
            vastauslista[f"vastaus{random_lista[3]}"] = vaarat_vastaukset[2][0], 0

        #KYSYMYS: LENTOKENTTIEN VÄLINEN ETÄISYYS
        elif kysymysvalinta == 4:
            question_text = ["What is the distance between ", " airports in kilometers?"]
            #Haetaan kysymykseen muuttujat
            sql = f"SELECT name, ident, latitude_deg, longitude_deg FROM airport ORDER BY RAND() LIMIT 2"
            kursori = yhteys.cursor()
            kursori.execute(sql)
            kysymys = kursori.fetchall()

            #Lasketaan kahden haetun lentokentän etäisyys
            start = [kysymys[0][2], kysymys[0][3]]
            end = [kysymys[1][2], kysymys[1][3]]

            #Oikea vastaus palautetaan kokonaislukuna
            oikea_vastaus = [int(distance.distance((start[0], start[1]), (end[0], end[1])).km)]

            #Luodaan random luvut vääriksi vastauksiksi
            vaarat_vastaukset = [random.randint(0,10000), random.randint(0,10000), random.randint(0,10000)]

            # Luodaan vastauslista, jossa vastauksen järjestys määräytyy random_listan mukaan
            vastauslista[f"vastaus{random_lista[0]}"] = oikea_vastaus[0], 1
            vastauslista[f"vastaus{random_lista[1]}"] = vaarat_vastaukset[0], 0
            vastauslista[f"vastaus{random_lista[2]}"] = vaarat_vastaukset[1], 0
            vastauslista[f"vastaus{random_lista[3]}"] = vaarat_vastaukset[2], 0

    #Jos kierrosnumero on alle 16, valitaan kysymys vaikeista kysymyksistä
    elif i < 16:
        #Luodaan vaikea kysymys
        kysymysvalinta = random.randint(1, 5)

        #KYSYMYS: MINKÄ LENTOKENTÄN ICAO KOODI ON?
        if kysymysvalinta == 1:
            question_text = ["Which airport has the ICAO code of ", "?"]
            # Haetaan kysymykseen muuttuja
            sql = f"SELECT ident FROM airport ORDER BY RAND() LIMIT 1"
            kursori = yhteys.cursor()
            kursori.execute(sql)
            # Haun tulos muuttujaan
            kysymys = kursori.fetchone()

            # Haetaan kysymykseen vastaus
            sql = f"SELECT name FROM airport WHERE ident = '{kysymys[0]}'"
            kursori = yhteys.cursor()
            kursori.execute(sql)
            # Oikea vastaus muuttujaan
            oikea_vastaus = kursori.fetchone()

            # Haetaan 3 väärää vastausta
            sql = f"SELECT name FROM airport WHERE NOT ident = '{kysymys[0]}' ORDER BY RAND() LIMIT 3"
            kursori = yhteys.cursor()
            kursori.execute(sql)
            # Väärät vastaukset muuttujaan
            vaarat_vastaukset = kursori.fetchall()

            # Luodaan vastauslista, jossa vastauksen järjestys määräytyy random_listan mukaan
            vastauslista[f"vastaus{random_lista[0]}"] = oikea_vastaus[0], 1
            vastauslista[f"vastaus{random_lista[1]}"] = vaarat_vastaukset[0][0], 0
            vastauslista[f"vastaus{random_lista[2]}"] = vaarat_vastaukset[1][0], 0
            vastauslista[f"vastaus{random_lista[3]}"] = vaarat_vastaukset[2][0], 0

        #KYSYMYS: MISSÄ LENTOKENTTÄ SIJAITSEE (AF/AS)
        elif kysymysvalinta == 2:
            question_text = ["What country is ", " located in?"]
            # Haetaan kysymykseen muuttuja
            sql = f"SELECT name, ident FROM airport WHERE continent = 'AF' OR continent = 'AS' ORDER BY RAND() LIMIT 1"
            kursori = yhteys.cursor()
            kursori.execute(sql)
            # Haun tulos muuttujaan
            kysymys = kursori.fetchone()

            # Haetaan kysymykseen vastaus
            sql = f"SELECT name, iso_country FROM country WHERE iso_country in(SELECT iso_country FROM airport WHERE ident = '{kysymys[1]}')"
            kursori = yhteys.cursor()
            kursori.execute(sql)
            # Oikea vastaus muuttujaan
            oikea_vastaus = kursori.fetchone()

            # Haetaan 3 väärää vastausta
            sql = f"SELECT name FROM country WHERE NOT iso_country = '{oikea_vastaus[1]}' ORDER BY RAND() LIMIT 3"
            kursori = yhteys.cursor()
            kursori.execute(sql)
            # Väärät vastaukset muuttujaan
            vaarat_vastaukset = kursori.fetchall()

            # Luodaan vastauslista, jossa vastauksen järjestys määräytyy random_listan mukaan
            vastauslista[f"vastaus{random_lista[0]}"] = oikea_vastaus[0], 1
            vastauslista[f"vastaus{random_lista[1]}"] = vaarat_vastaukset[0][0], 0
            vastauslista[f"vastaus{random_lista[2]}"] = vaarat_vastaukset[1][0], 0
            vastauslista[f"vastaus{random_lista[3]}"] = vaarat_vastaukset[2][0], 0

        #KYSYMYS: KUINKA KORKEALLA LENTOKENTTÄ SIJAITSEE? (AF/AS)
        elif kysymysvalinta == 3:
            question_text = ["What is the elevation of ", " airport?"]
            # Haetaan kysymykseen muuttuja
            sql = f"SELECT name, ident FROM airport WHERE continent = 'AF' OR continent = 'AS' ORDER BY RAND() LIMIT 1"
            kursori = yhteys.cursor()
            kursori.execute(sql)
            # Haun tulos muuttujaan
            kysymys = kursori.fetchone()

            sql = f"SELECT elevation_ft*0.3048 as elevation_m FROM airport WHERE ident = '{kysymys[1]}'"
            kursori = yhteys.cursor()
            kursori.execute(sql)
            # Oikea vastaus muuttujaan
            oikea_vastaus = kursori.fetchone()

            # Haetaan 3 väärää vastausta
            sql = f"SELECT elevation_ft*0.3048 as elevation_m FROM airport WHERE NOT ident = '{kysymys[1]}' ORDER BY RAND() LIMIT 3"
            kursori = yhteys.cursor()
            kursori.execute(sql)
            # Väärät vastaukset muuttujaan
            vaarat_vastaukset = kursori.fetchall()

            # Luodaan vastauslista, jossa vastauksen järjestys määräytyy random_listan mukaan
            vastauslista[f"vastaus{random_lista[0]}"] = oikea_vastaus[0], 1
            vastauslista[f"vastaus{random_lista[1]}"] = vaarat_vastaukset[0][0], 0
            vastauslista[f"vastaus{random_lista[2]}"] = vaarat_vastaukset[1][0], 0
            vastauslista[f"vastaus{random_lista[3]}"] = vaarat_vastaukset[2][0], 0

        # KYSYMYS: MIKÄ ON LENTOKENTÄN GPS-KOODI (EU/US)
        elif kysymysvalinta == 4:
            question_text = ["What is the GPS Code of ", "?"]
            # Haetaan kysymykseen muuttuja
            sql = f"SELECT name, ident FROM airport WHERE (gps_code <> '') AND (continent = 'EU' OR continent = 'US') ORDER BY RAND() LIMIT 1"
            kursori = yhteys.cursor()
            kursori.execute(sql)
            # Haun tulos muuttujaan
            kysymys = kursori.fetchone()

            #Haetaan oikea vastaus
            sql = f"SELECT gps_code FROM airport WHERE ident = '{kysymys[1]}' AND gps_code <> ''"
            kursori = yhteys.cursor()
            kursori.execute(sql)
            # Oikea vastaus muuttujaan
            oikea_vastaus = kursori.fetchone()

            # Haetaan 3 väärää vastausta
            sql = f"SELECT gps_code FROM airport WHERE NOT ident = '{kysymys[1]}' AND gps_code != '' ORDER BY RAND() LIMIT 3"
            kursori = yhteys.cursor()
            kursori.execute(sql)
            # Väärät vastaukset muuttujaan
            vaarat_vastaukset = kursori.fetchall()

            # Luodaan vastauslista, jossa vastauksen järjestys määräytyy random_listan mukaan
            vastauslista[f"vastaus{random_lista[0]}"] = oikea_vastaus[0], 1
            vastauslista[f"vastaus{random_lista[1]}"] = vaarat_vastaukset[0][0], 0
            vastauslista[f"vastaus{random_lista[2]}"] = vaarat_vastaukset[1][0], 0
            vastauslista[f"vastaus{random_lista[3]}"] = vaarat_vastaukset[2][0], 0

        #KYSYMYS: PALJON PÄÄSTÖJÄ MATKASTA
        elif kysymysvalinta == 5:
            question_text = ["How many kilotons of CO2 emmission are produced on a flight between ", " airports on Airbus A320?"]
            #Haetaan kysymykseen muuttujat
            sql = f"SELECT name, ident, latitude_deg, longitude_deg FROM airport ORDER BY RAND() LIMIT 2"
            kursori = yhteys.cursor()
            kursori.execute(sql)
            kysymys = kursori.fetchall()

            #Lasketaan kahden haetun lentokentän etäisyys
            start = [kysymys[0][2], kysymys[0][3]]
            end = [kysymys[1][2], kysymys[1][3]]

            #Oikea vastaus palautetaan kokonaislukuna
            oikea_vastaus = [int(distance.distance((start[0], start[1]), (end[0], end[1])).km)]

            #Luodaan random luvut vääriksi vastauksiksi
            vaarat_vastaukset = [random.randint(0,10000), random.randint(0,10000), random.randint(0,10000)]

            # Luodaan vastauslista, jossa vastauksen järjestys määräytyy random_listan mukaan
            vastauslista[f"vastaus{random_lista[0]}"] = oikea_vastaus[0]*9, 1
            vastauslista[f"vastaus{random_lista[1]}"] = vaarat_vastaukset[0]*9, 0
            vastauslista[f"vastaus{random_lista[2]}"] = vaarat_vastaukset[1]*9, 0
            vastauslista[f"vastaus{random_lista[3]}"] = vaarat_vastaukset[2]*9, 0

    # Jos saavutetaan maksimi-kierrokset, pelaaja on voittaja, ei luoda kysymystä
    else:
        return "winner"

    # Palautetaan funktiosta sanakirja, joka sisältää kysymyksen, vastaukset ja tiedon onko vastaus oikein vai väärin
    return {
        "vastaus1": ["A", vastauslista["vastaus1"][0], vastauslista["vastaus1"][1]],
        "vastaus2": ["B", vastauslista["vastaus2"][0], vastauslista["vastaus2"][1]],
        "vastaus3": ["C", vastauslista["vastaus3"][0], vastauslista["vastaus3"][1]],
        "vastaus4": ["D", vastauslista["vastaus4"][0], vastauslista["vastaus4"][1]],
        "kysymys": kysymys,
        "kysymysteksti": question_text
    }

#High Score -funktio, joka printtaa Top 10 -pelaajaa tietokannasta
def highscore():
    #Haetaan pelaajien nimet ja pisteet taulusta, järjestetään ne ja rajoitetaan vain 10 parhaaseen tulokseen
    sql = f"SELECT name, score FROM highscores ORDER BY score DESC LIMIT 10"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    #Printataan jokainen rivi listaamaan top 10 -pelaajat
    for rivi in tulos:
        print(f"Name: {rivi[0]}, Score: {rivi[1]}")
    return

#Score Insert -funktio, jolla pelaajan pisteet lisätään pelin jälkeen
def scoreinsert(username, money):
    mycursor = yhteys.cursor()
    #Lisätään pelaajan nimi ja pisteet highscores -tauluun
    sql = f"INSERT INTO highscores (name, score) VALUES (%s, %s)"
    val = (username, money)
    mycursor.execute(sql, val)
    yhteys.commit()

#Oljenkorsi -funktio, jossa pelaaja valitsee oljenkorren helpoittaakseen peliä
def oljenkorret(kysymys_sanakirja, olki1, olki2, olki3):
    #Printataan lista oljenkorsista jotka ovat käytössä
    print("\nLifelines:")
    if olki1 == False:
        print("1. Ask the audience")
    if olki2 == False:
        print("2. Eliminate 2 wrong answers")
    if olki3 == False:
        print("3. Call a friend")
    valinta = input("Choose a lifeline (1/2/3): ")

    #Jos valitaan oljenkorsi 1.
    if valinta == "1":
        if olki1 == False:
            olki1 = True
            # Kysy yleisöltä
            yleison_mielipide = {
                "A": random.randint(0, 60),
                "B": random.randint(0, 60),
                "C": random.randint(0, 60),
                "D": random.randint(0, 60),
            }
            oikea_vastaus_kirjain = ""
            for i in kysymys_sanakirja:
                if kysymys_sanakirja[i][2] == 1:
                    oikea_vastaus_kirjain = kysymys_sanakirja[i][0]
                    break

            yleison_mielipide[oikea_vastaus_kirjain] = random.randint(40,90)

            print("\nAudience thinks it is:")
            for kirjain, prosentti in yleison_mielipide.items():
                if kirjain == "A":
                    print(f"A: {prosentti} votes")
                elif kirjain == "B":
                    print(f"B: {prosentti} votes")
                elif kirjain == "C":
                    print(f"C: {prosentti} votes")
                elif kirjain == "D":
                    print(f"D: {prosentti} votes")
            # Printataan kysymys ja vaihtoehdot uudelleen
            vastausvalikko(kysymys_sanakirja)

    #Jos valitaan oljenkorsi 2.
    elif valinta == "2":
        if olki2 == False:
            olki2 = True
            oikea_vastaus_kirjain = ""
            for i in kysymys_sanakirja:
                if kysymys_sanakirja[i][2] == 1:
                    oikea_vastaus_kirjain = i
                    break

            poistettavat_kirjaimet = []
            for kirjain in kysymys_sanakirja:
                if kirjain != "kysymys":
                    if kirjain != "kysymysteksti":
                        if kirjain != oikea_vastaus_kirjain:
                            poistettavat_kirjaimet.append(kirjain)

            poistettavat_kirjaimet = random.sample(poistettavat_kirjaimet, 2)

            print("\n2 wrong answers have been eliminated:")
            if kysymys_sanakirja["kysymysteksti"][0] == "What is the distance between ":
                print(f"{kysymys_sanakirja["kysymysteksti"][0]}{kysymys_sanakirja['kysymys'][0][0]} and {kysymys_sanakirja['kysymys'][1][0]}{kysymys_sanakirja["kysymysteksti"][1]}")
            else:
                print(f"{kysymys_sanakirja["kysymysteksti"][0]}{kysymys_sanakirja['kysymys'][0]}{kysymys_sanakirja["kysymysteksti"][1]}")
            for kirjain in kysymys_sanakirja:
                if kirjain not in poistettavat_kirjaimet:
                    if kirjain == "vastaus1":
                        print(f"A: {kysymys_sanakirja["vastaus1"][1]}")
                    elif kirjain == "vastaus2":
                        print(f"B: {kysymys_sanakirja["vastaus2"][1]}")
                    elif kirjain == "vastaus3":
                        print(f"C: {kysymys_sanakirja["vastaus3"][1]}")
                    elif kirjain == "vastaus4":
                        print(f"D: {kysymys_sanakirja["vastaus4"][1]}")

    #Jos valitaan oljenkorsi 3.
    elif valinta == "3":
        if olki3 == False:
            olki3 = True
            # Soita kaverille
            kaverin_vastaus = ""
            error_margin = random.randint(1,100)

            if error_margin <= 50:
                for i in kysymys_sanakirja:
                    if kysymys_sanakirja[i][2] == 1:
                        kaverin_vastaus = kysymys_sanakirja[i][1]
                        break
            else:
                for i in kysymys_sanakirja:
                    if kysymys_sanakirja[i][2] == 0:
                        kaverin_vastaus = kysymys_sanakirja[i][1]
                        break

            print("\nFriends answer:")
            print(f"I think the answer is: {kaverin_vastaus}")
            # Printataan kysymys ja vaihtoehdot uudelleen
            vastausvalikko(kysymys_sanakirja)

    #Jos syötteessä on virhe
    else:
        print("Incorrect input.")
        #Printataan kysymys ja vaihtoehdot uudelleen
        vastausvalikko(kysymys_sanakirja)

    return kysymys_sanakirja, olki1, olki2, olki3

#Palkinto -funktio, koska palkintomäärät eivät seuraa yhtä matemaattista kaavaa
def prizecalc(current_round):
    if current_round == 2:
        return 100
    elif current_round == 3:
        return 200
    elif current_round == 4:
        return 300
    elif current_round == 5:
        return 500
    elif current_round == 6:
        return 1000
    elif current_round == 7:
        return 2000
    elif current_round == 8:
        return 4000
    elif current_round == 9:
        return 8000
    elif current_round == 10:
        return 16000
    elif current_round == 11:
        return 32000
    elif current_round == 12:
        return 64000
    elif current_round == 13:
        return 125000
    elif current_round == 14:
        return 250000
    elif current_round == 15:
        return 500000
    elif current_round == 16:
        return 1000000
    return None

#Peliprosessi, jota kutsutaan pelin käynnistämiseksi
def game():
    # Muuttuja joka määrittää kysytäänkö kysymyksiä
    game_over = False
    olki1 = False
    olki2 = False
    olki3 = False
    username = ""

    # Pelaajan raha
    money = 0

    #Peli-loop
    while game_over == False:
        #Alkuteksti
        for line in tarina.getStory():
            print(line)
        print("")
        print("Type [START] to start the game.")
        print("Type [SCORES] to see the highscores.")
        valinta = input("[START]/[SCORES]: ").upper()

        #Tulostetaan high score -taulu
        while valinta == "SCORES":
            highscore()
            valinta = input("[START]/[SCORES]: ").upper()

        #Pelin käynnistys
        if valinta == "START":
            username = input('Enter your username: ')

            #Pelaajan edistyminen
            current_round = 1

            #Peli-loop
            while current_round < 17:
                #Ajetaan funktio joka täyttää kysymys-sanakirjan
                kysymys_sanakirja = kysymysfunktio(current_round)

                #Jos funktio palauttaa arvon "winner", pelaaja voittaa
                if kysymys_sanakirja == "winner":
                    print("You have won!")
                    game_over = True
                    break
                #Muutoin funktio palauttaa kysymys-sanakirjan
                else:
                    #Nykyinen palkintomäärä
                    print(f"You have earned {money}€")
                    #DEV CHEATS
                    #print(kysymys_sanakirja)

                    #Printataan kysymys ja vastaukset
                    vastausvalikko(kysymys_sanakirja)

                    #Jos oljenkorsia on jäljellä, printataan ohje käyttää niitä
                    if olki1 == False or olki2 == False or olki3 == False:
                        print(f"E. Use a lifeline")

                    #Vastauskenttä
                    vastaus = input('Enter your answer: ').upper()

                    #Vastauksen tarkistuksen muuttuja
                    vastausmuuttuja = ""

                    #Tarkistetaan minkä vastauksen pelaaja syötti
                    if vastaus == kysymys_sanakirja["vastaus1"][0]:
                        vastausmuuttuja = "vastaus1"
                    elif vastaus == kysymys_sanakirja["vastaus2"][0]:
                        vastausmuuttuja = "vastaus2"
                    elif vastaus == kysymys_sanakirja["vastaus3"][0]:
                        vastausmuuttuja = "vastaus3"
                    elif vastaus == kysymys_sanakirja["vastaus4"][0]:
                        vastausmuuttuja = "vastaus4"

                    #Tarkistetaan onko pelaajan syöte yksi kysymyksen vastauksista
                    if vastausmuuttuja in kysymys_sanakirja:
                        #Jos vastaus on oikein
                        if kysymys_sanakirja[vastausmuuttuja][2] == 1:
                            print("This answer is correct!")
                            current_round += 1
                            money = prizecalc(current_round)
                        #Jos vastaus on väärin
                        else:
                            print("This answer is incorrect!")
                            game_over = True
                            break

                    #Jos pelaaja haluaa käyttää oljenkorren
                    elif vastaus == "E":
                        #Tarkistetaan onko pelaajalla oljenkorsia
                        if olki1 == True & olki2 == True & olki3 == True:
                            print("Incorrect input; you have no lifelines.")
                            game_over = True
                            break

                        #Jos oljenkorsia on jäljellä
                        else:
                            #Ajetaan oljenkorsi-funktio
                            kysymys_sanakirja, olki1, olki2, olki3 = oljenkorret(kysymys_sanakirja, olki1, olki2, olki3)

                            #Kysytään kysymyksen vastaus uudelleen
                            vastaus = input('Enter your answer: ').upper()

                            #Vastauksen tarkistuksen muuttuja
                            vastausmuuttuja = ""

                            # Tarkistetaan minkä vastauksen pelaaja syötti
                            if vastaus == kysymys_sanakirja["vastaus1"][0]:
                                vastausmuuttuja = "vastaus1"
                            elif vastaus == kysymys_sanakirja["vastaus2"][0]:
                                vastausmuuttuja = "vastaus2"
                            elif vastaus == kysymys_sanakirja["vastaus3"][0]:
                                vastausmuuttuja = "vastaus3"
                            elif vastaus == kysymys_sanakirja["vastaus4"][0]:
                                vastausmuuttuja = "vastaus4"

                            #Tarkistetaan onko pelaajan syöte yksi kysymyksen vastauksista
                            if vastausmuuttuja in kysymys_sanakirja:
                                #Jos vastaus on oikein
                                if kysymys_sanakirja[vastausmuuttuja][2] == 1:
                                    print("This answer is correct!")
                                    current_round += 1
                                    money = prizecalc(current_round)
                                #Jos vastaus on väärin
                                else:
                                    print("This answer is incorrect!")
                                    game_over = True
                                    break

                            #Jos pelaaja kirjoittaa väärin, tai yrittää valita oljenkorren uudelleen
                            else:
                                print("Invalid answer!")
                                game_over = True
                                break

                    #Jos pelaaja kirjoittaa väärin
                    else:
                        print("Invalid answer!")
                        game_over = True
                        break
            #Kun pelaajan kierrokset täyttyvät, tai pelaaja vastaa väärin, poistutaan peli-loopista
            break
        else:
            print("Incorrect input.")
            game_over = True
            break
    #Jos pelaaja vastaa väärin, palataan pois funktiosta
    if game_over == True:
        print(f"Your winnings are {money}€")

        #Jäljellä olevien oljenkorsien antama bonus
        lifeline_bonus = 0
        if olki1 == False:
            lifeline_bonus += current_round * 100
        if olki2 == False:
            lifeline_bonus += current_round * 100
        if olki3 == False:
            lifeline_bonus += current_round * 100

        print(f"Un-used Lifeline Bonus: {lifeline_bonus}")
        #Lisätään bonus rahoihin
        money += lifeline_bonus

        print(f"Your total winnings are {money}€")
        print("GAME OVER!")
        # Lisätään highscore tiedot tietokantaan
        scoreinsert(username, money)
        return game_over

#Aloitetaan peli-funktio
game_over = game()

while game_over == True:
    #Kysytään haluaako pelaaja käynnistää pelin uudelleen
    restart = input('Do you want to try again? (y/n): ').upper()
    if restart == 'Y':
        game()
    elif restart == 'N':
        exit()

