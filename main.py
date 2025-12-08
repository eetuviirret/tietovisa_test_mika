import random
import mysql.connector
import tarina
from geopy import distance
from flask import Flask, Response, request, jsonify
from flask_cors import CORS
import json

#SQL yhteys
yhteys = mysql.connector.connect(
    host='localhost',
    port=3306, #3306 jos sinne asennettu MySQL
    database='flight_game',
    user='root',
    password='Sorsalampi2025', #KÄYTTÄJÄN SALASANA
    autocommit=True
)
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
@app.route('/<i>', methods=['GET'])

#Kysymys -funktio, joka asettaa sanakirjaan kysymyksen ja vastaukset
def kysymysfunktio(i):
    # Sanakirja, johon vastaukset talletetaan
    vastauslista = {}

    # Lista joka asettaa oikeat ja väärät vastaukset satunnaiseen järjestykseen
    random_lista = ["1", "2", "3", "4"]
    random.shuffle(random_lista)

    #Jos kierrosnumero on alle 6, valitaan kysymys helpoista kysymyksistä
    if int(i) < 6:
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
    elif int(i) < 11:
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
    elif int(i) < 16:
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

    jsonvast = {
        "vastaus1": ["A", vastauslista["vastaus1"][0], vastauslista["vastaus1"][1]],
        "vastaus2": ["B", vastauslista["vastaus2"][0], vastauslista["vastaus2"][1]],
        "vastaus3": ["C", vastauslista["vastaus3"][0], vastauslista["vastaus3"][1]],
        "vastaus4": ["D", vastauslista["vastaus4"][0], vastauslista["vastaus4"][1]],
        "kysymys": kysymys,
        "kysymysteksti": question_text
    }
    response = jsonify(jsonvast)
    response.headers.add('Access-Control-Allow-Origin', '*')


    # Palautetaan funktiosta sanakirja, joka sisältää kysymyksen, vastaukset ja tiedon onko vastaus oikein vai väärin
    return response


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=3000)
