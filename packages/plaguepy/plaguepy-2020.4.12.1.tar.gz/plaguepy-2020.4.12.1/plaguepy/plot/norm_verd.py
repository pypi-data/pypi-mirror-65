import matplotlib.pyplot as plt  # Voor de grafieken
import numpy as np  # Om data als arrays op te kunnen slaan en de normale verdeling te kunnen tekenen
import seaborn as sns
from scipy.spatial import Voronoi
from scipy.stats import norm  # Om de lijn van de normale verdeling te tekenen. Getallen zijn zelf berekend.

from plaguepy import bereken

sns.set()


def normale_verdeling(mu: float, sigma: float, mid_afstand: float, labels: tuple) -> None:
    """Plot-code afgeleid van: Thijs van den Berg (Jun. 2019).
    https://github.com/Denbergvanthijs/AC-opdrachten/

    Mu en sigma zijn vaak 0 resp. 1
    mid_afstand is de hemelsbrede afstand naar het middelpunt vanaf een punt

    :param mu: gemiddelde van de normale verdelingen
    :param sigma: standaard deviatie van de normale verdelingen
    :param mid_afstand: Afstand van de twee punten tot het middelpunt
    :param labels: Lijst van twee strings, labels[0] is de naam van eerste verdeling, idem voor labels[1]

    :returns: Plot met twee normale verdelingen. In de titel het percentage dat zij overlappen en de meegegeven afstand tot het middelpunt.
    """
    if not isinstance(mu, (int, float)) or not isinstance(sigma, (int, float)) \
            or not isinstance(mid_afstand, (int, float)) or not isinstance(labels, (list, tuple)):
        raise ValueError("Verkeerde waardes meegegeven als argumenten")

    if len(labels) != 2:
        raise ValueError("Lijst/tuple `labels` moet twee elementen bevatten")

    plt.rcParams['figure.figsize'] = [9, 6]  # Grotere plots in Jupyter Notebook
    percentage_overlap = bereken.perc_overlap(mid_afstand, mu, sigma)
    lijn = np.linspace(mu - 4 * sigma - mid_afstand,
                       mu + 4 * sigma + mid_afstand)  # De lengte van de lijn van normale verdelingen

    plt.plot(lijn, norm.pdf(lijn, mu - mid_afstand, sigma), label=labels[0])  # De linker normale verdeling
    plt.plot(lijn, norm.pdf(lijn, mu + mid_afstand, sigma), label=labels[1])  # De rechter normale verdeling
    plt.axvline(x=mu, color="black", linestyle='--', label='Middelpunt')

    plt.xlim(mu - 3 * sigma - mid_afstand,
             mu + 3 * sigma + mid_afstand)  # Tenminste 99,8% zichtbaar van beide verdelingen
    plt.ylim(bottom=0)
    plt.xlabel("Aantal Standaard Deviaties")
    plt.ylabel("Kans")
    plt.title(f"{percentage_overlap * 100:.2f}% overlapt in totaal.\nAfstand tot het middelpunt: {mid_afstand:.2f} SD.")
    plt.legend()
    plt.tight_layout()  # Zodat ook de astitels op de grafieken passen
    plt.show()


def normale_verdeling_compleet(punten: np.ndarray) -> None:
    """Plot de normale verdelingen van alle mogelijke combinaties van punten.
    Een zichtbare Voronoi is niet nodig om berekeningen uit te voeren.
    De voronoi wordt echter wel gebruikt om de punten te berekenen.

    :param punten: Numpy array van n bij 2. Iedere row bevat een x en y coördinaat.
    :returns: Alle mogelijke plots met twee normale verdelingen.
              In de titel het percentage dat zij overlappen
              en de meegegeven afstand tot het middelpunt.
              Normale verdelingen die minder dan 0.00% overlappen worden niet geplot.

    """
    if not isinstance(punten, np.ndarray):
        raise ValueError("Verkeerde waardes meegegeven als argumenten")

    vor = Voronoi(punten)
    mid_afstanden = bereken.middelpunt_afstanden(punten)

    for i, punt in enumerate(mid_afstanden):
        normale_verdeling(0, 1, punt, tuple(vor.points[vor.ridge_points[i]]))
