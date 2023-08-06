import os
import time

import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut


def straat2coord(file_path: str, woonplaats: str, woonplaats_header: str, adres_header: str, sep: str = ";") -> None:
    """Berekend aan de hand van een CSV-bestand de breedte- en hoogtegraad.
    Resultaten worden opgeslagen in een nieuw CSV-bestand `data/geoDataKDV.csv`.
    Als input wordt om een woonplaats gevraagd. Alle punten die aan de waarde 'woonplaats voldoen'
    in de kolom 'woonplaatsHeader' worden geimporteerd.

    De breedte- en lengtegraad van de waardes die zich bevinden in de kolom 'adresHeader' worden opgevraagd.
    Duplicaten worden direct overgeslagen.

    :param file_path: totale path naar het te converteren bestand
    :param woonplaats: woonplaats waar een selectie uit (landelijke) data word gehaald
    :param woonplaats_header: kolom waar de waarde `woonplaats` zich in bevind
    :param adres_header: kolom met de adressen die omgezet mooeten worden. Idealieter adres + huisnummer
    :param sep: separator voor CSV-bestand, standaard ';' maar kan ook ',' of iets anders zijn

    :returns: Geconverteerd bestand opgeslagen in data/output/. Bestand bevat de headers latitude en longitude
    """
    if not isinstance(file_path, str) or not isinstance(woonplaats, str) \
            or not isinstance(woonplaats_header, str) or not isinstance(adres_header, str):
        raise ValueError("Verkeerde waardes meegegeven als argumenten")

    print("Even geduld a.u.b, dit kan even duren...")
    csv_data = pd.read_csv(file_path, sep=sep)  # Data uitlezen uit bestand
    subset = csv_data.loc[csv_data[woonplaats_header] == woonplaats]  # Selectie maken van de data

    geo_locator = Nominatim(user_agent="IPASS Project - Thijs van den Berg 2019")  # Variabele opzetten voor API-calls
    geo_locaties = pd.DataFrame(columns=['latitude', 'longitude'])  # DataFrame

    for adres in subset[adres_header].drop_duplicates():  # Ieder adres omzetten naar coördinaten
        try:
            locatie = geo_locator.geocode(f"{adres} {woonplaats}")  # Coordinaten opzoeken
        except GeocoderTimedOut:  # Te veel requests
            locatie = None

        if locatie is not None:
            geo_locaties = geo_locaties.append({'latitude': locatie.latitude, 'longitude': locatie.longitude},
                                               ignore_index=True)

        time.sleep(0.5)  # ToManyRequestsError tegengaan

    abs_path = os.path.basename(file_path)
    file_name = os.path.splitext(abs_path)[0]

    geo_locaties.to_csv(f"data/output/geo_{file_name}.csv", index=False)  # Data opslaan tbv de snelheid
    print(geo_locaties.head())


def coord2coord(file_path: str, lat_header: str, long_header: str) -> None:
    """Haalt uit een CSV-bestand de latitude- en longitudekolom.
    De gebruiker dient de namen van de kolommen waarde latitude en logitude
    zijn opgeslagen op te geven.
    Deze kolommen worden opgeslagen in een nieuw bestand met de prefix `geo_`.

    Het bestand kan vervolgens worden gebruikt om Voronoi's of kaarten te maken.

    :param file_path: totale path naar het te converteren bestand
    :param lat_header: naam van de kolom die de latitude bevat
    :param long_header: naam van de kolom die de longiutde bevat

    :returns: Geconverteerd bestand opgeslagen in data/output/. Bestand bevat de headers latitude en longitude
    """
    if not isinstance(file_path, str) or not isinstance(lat_header, str) \
            or not isinstance(long_header, str):
        raise ValueError("Verkeerde waardes meegegeven als argumenten")

    print("Even geduld a.u.b, dit kan even duren...")
    csv_data = pd.read_csv(file_path, sep=";")  # Data uitlezen uit bestand

    geo_locaties = csv_data[[lat_header, long_header]].rename(
        columns={lat_header: "latitude", long_header: "longitude"})  # Twee kolommen uit de data halen en hernoemen

    abs_path = os.path.basename(file_path)
    file_name = os.path.splitext(abs_path)[0]

    geo_locaties.to_csv(f"data/output/geo_{file_name}.csv", index=False)  # Data opslaan tbv de snelheid
    print(geo_locaties.head())
