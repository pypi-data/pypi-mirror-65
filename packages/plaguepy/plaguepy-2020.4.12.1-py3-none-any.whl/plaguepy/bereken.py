import math

import numpy as np  # Om data als arrays op te kunnen slaan en de normale verdeling te kunnen tekenen
import pandas as pd
from scipy.spatial import Voronoi
from scipy.stats import norm  # Om de lijn van de normale verdeling te tekenen. Getallen zijn zelf berekend.


def perc_overlap(mid_afstand: float, mu: float, sigma: float) -> float:
    """Berekend het percentage overlap tussen twee punten.
    norm.cdf(-n) berekend de kans tot n SD.
    In de wiskunde wordt vaak (1 - norm.cdf(n)) i.p.v. bovenstaande

    Door deze waarde maal twee te doen hebben we de totale overlapping.

    :param mid_afstand: Afstand van de twee punten tot het middelpunt
    :param mu: gemiddelde van de normale verdelingen
    :param sigma: standaard deviatie van de normale verdelingen
    :returns: het totale percentage dat de twee normale verdelingen elkaar overlappen. 0 < perc < 1
    """
    if not isinstance(mid_afstand, (int, float)) or not isinstance(mu, (int, float)) \
            or not isinstance(sigma, (int, float)):
        raise ValueError("Verkeerde waardes meegegeven als argumenten")

    if sigma <= 0:
        raise ValueError("Sigma kan niet negatief zijn")

    return norm.cdf(-mid_afstand + mu, loc=mu, scale=sigma) * 2


def perc_overlap_matrix(punten: np.ndarray, mu: float, sigma: float) -> np.ndarray:
    """
    :param punten: Numpy array van n bij 2. Iedere row bevat een x en y coördinaat.
    :param mu: gemiddelde van de normale verdelingen
    :param sigma: standaard deviatie van de normale verdelingen
    :returns: matrix van n bij n met alle percentages dat de punten overlappen
    """
    if not isinstance(punten, np.ndarray) or not isinstance(mu, (int, float)) \
            or not isinstance(sigma, (int, float)):
        raise ValueError("Verkeerde waardes meegegeven als argumenten")

    output_matrix = []

    for punt1 in punten:
        for punt2 in punten:
            middelpunt = abs((punt2 - punt1) / 2)  # [A, B]

            middelpunt_afstand = np.sqrt(  # Wortel van [A^2 + B^2]
                np.sum(  # ΔA^2 + ΔB^2
                    np.square(  # Macht van ΔA en ΔB
                        middelpunt)))  # [ΔA, ΔB]

            output_matrix.append(perc_overlap(middelpunt_afstand, mu, sigma))

    return np.array(output_matrix).reshape(len(punten), len(punten))


def grens(grens_perc: float, mu: float, sigma: float) -> float:
    """Berekend het aantal standaard deviaties dat nodig is om op een bepaalde cumulatieve kans te komen.
    Dezelfde functie als invNorm op de Texas Instruments grafische rekenmachines.
    0.00 < grens < 1.00
    Kan gebruikt worden om de hoogte van de Ellipse in Voronoi-diagrammen te bepalen

    :param grens_perc: getal tussen 0 en 1. Stel grens_waarde is 0.2 dan wordt het aantal standaard deviaties van mu(50%) tot 20% berekend.
    :param mu: gemiddelde van de normale verdelingen
    :param sigma: standaard deviatie van de normale verdelingen
    :return: het aantal standaard deviaties van mu tot de grens_waarde
    """
    if not isinstance(grens_perc, (int, float)) or not isinstance(mu, (int, float)) \
            or not isinstance(sigma, (int, float)):
        raise ValueError("Verkeerde waardes meegegeven als argumenten")

    if grens_perc >= 1 or grens_perc <= 0:
        raise ValueError("Grens kan niet meer dan 100%, negatief of 0 zijn")

    return norm.ppf(grens_perc, loc=mu, scale=sigma)


def helling(punt1: np.ndarray, punt2: np.ndarray) -> float:
    """Berekend de helling in graden tussen twee coordinaten.
    Kan gebruikt worden om de richting van de Ellipse in Voronoi-diagrammen te bepalen.

    :param punt1: Numpy array met een enkele row: [x, y]
    :param punt2: Numpy array met een enkele row: [x, y]
    :return: de hoek in aantal graden tussen punt1 en punt2
    """
    if not isinstance(punt1, np.ndarray) or not isinstance(punt2, np.ndarray):
        raise ValueError("Verkeerde waardes meegegeven als argumenten")

    delta = punt2 - punt1

    if delta[0] != 0.0:  # ZeroDivisionError voorkomen
        richtings_coefficient = delta[1] / delta[0]
        return math.degrees(math.atan(richtings_coefficient))
    else:
        return -90


def middelpunt_afstanden(punten: np.ndarray) -> list:
    """Berekend de afstand tot het middelpunt voor iedere combinatie van twee punten.
    Input is een np.array() van N bij 2.
    Gebaseerd op: https://github.com/scipy/scipy/blob/master/scipy/spatial/_plotutils.py

    :param punten: Numpy array van n bij 2. Iedere row bevat een x en y coördinaat.
    :return: lijst van afstanden tussen alle belanghebbende punten
    """
    if not isinstance(punten, (np.ndarray, pd.DataFrame)):
        raise ValueError("Verkeerde waardes meegegeven als argumenten")

    vor = Voronoi(punten)
    afstanden = []

    for punt in vor.ridge_points:
        middelpunt = vor.points[punt].mean(axis=0)

        mid_afstand = np.sqrt(  # Wortel van [A^2 + B^2]
            np.sum(  # ΔA^2 + ΔB^2
                np.square(  # Macht van ΔA en ΔB
                    middelpunt - vor.points[punt][0])))  # [ΔA, ΔB]

        afstanden.append(mid_afstand)
    return afstanden


def matrix_maal_matrix(m1: np.ndarray, m2: np.ndarray) -> np.ndarray:
    """Vermenigvuldigd matrix m maal n en zet alle waardes boven 1, op 1.
    Dit aangezien de 'infectiegraad' nooit meer dan 100% kan zijn.

    :param m1: matrix van n bij n
    :param m2: matrix van n bij n
    :return: matrix van n bij n, geen enkele waarde meer dan 1
    """
    if not isinstance(m1, np.ndarray) or not isinstance(m2, np.ndarray):
        raise ValueError("Verkeerde waardes meegegeven als argumenten")

    matrix = np.matmul(m1, m2)
    return np.where(matrix > 1, 1, matrix)


def perc_volledige_infectie(matrix_verloop: np.ndarray) -> tuple:
    """Berekend voor ieder punt in punten_matrix na hoeveel periodes deze volledig was geinfecteerd.
    Berekend vervolgens op hoeveel procent van de totale duur dat was.
    Iedere rij staat voor een punt. De lengte van de rij voor het aantal periodes.

    :param matrix_verloop: matrix van n bij m. n-aantal punten en m-aantal periodes

    :return: tuple met op hoeveel procent ieder punt volledig was geinfecteerd
    """
    if not isinstance(matrix_verloop, np.ndarray):
        raise ValueError("Verkeerde waardes meegegeven als argumenten")

    lijst = []

    for punt in matrix_verloop:
        voll_inf = np.where(punt == 1)  # Alle waardes waarbij het punt volledig is geinfecteerd

        try:
            lijst.append(voll_inf[0][0])  # Eerste waarde waarbij het punt volledig is geinfecteerd
        except IndexError:  # Als het punt nooit volledig is geinfecteerd
            if lijst:  # Als er al eerdere waardes zijn gegenereerd
                lijst.append(max(lijst))
            else:  # Als het de eerste waarde is
                lijst.append(1)

    return tuple((1 / max(lijst) * punt for punt in lijst))


def matrix_vec_verloop(punten: np.ndarray, vector: np.ndarray, perioden: int, mu: float = 0, sigma: float = 1) -> np.ndarray:
    """Berekend voor iedere stap in de tijd de matrix uit.
    Iedere stap wordt opgeslagen en vormen samen een n bij m matrix. N voor het aantal punten en m voor het aantal periodes.

    :param punten: Numpy array van n bij 2. Iedere row bevat een x en y coördinaat.
    :param vector: Numpy array van n bij 1. Bevat per cell 0 of 1. Iedere cell waar 1 staat, begint de infectie.
    :param perioden:  Het aantal perioden dat het verloop berekend en getoont moet worden.
    :param mu: gemiddelde van de normale verdelingen
    :param sigma: standaard deviatie van de normale verdelingen

    :return: n bij m matrix met het verloop. Kan worden geplot
    """
    if not isinstance(punten, np.ndarray) or not isinstance(vector, np.ndarray) or not isinstance(perioden, int) \
            or not isinstance(mu, (float, int)) or not isinstance(sigma, (float, int)):
        raise ValueError("Verkeerde waardes meegegeven als argumenten")

    if punten.shape[0] != vector.shape[0]:
        raise ValueError("Vector en punten moeten even lang zijn.")

    matrix_verloop = []
    matrix_percentages = perc_overlap_matrix(punten, mu, sigma)

    for periode in range(perioden + 1):  # Reken voor iedere periode het matrix vector dotproduct uit
        i = 0
        matrix = matrix_percentages.copy()
        while i != periode:
            matrix = matrix_maal_matrix(matrix, matrix_percentages)
            i += 1
        matrix_verloop.append(vector.dot(matrix))

    return np.vstack(matrix_verloop).T  # Maakt van een lijst met lijsten een numpy array
