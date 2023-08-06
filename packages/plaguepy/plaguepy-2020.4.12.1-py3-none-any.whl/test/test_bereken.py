import numpy as np
import pytest

from plaguepy import bereken


def test_perc_overlap():
    """Test de functie perc_overlap in bereken.py."""
    assert bereken.perc_overlap(0, 0, 1) == 1.0
    assert bereken.perc_overlap(0, 1, 1) == 1.0
    assert bereken.perc_overlap(1, 0, 1) == pytest.approx(0.3173105)
    assert bereken.perc_overlap(1, 1, 1) == pytest.approx(0.3173105)

    with pytest.raises(ValueError):
        assert bereken.perc_overlap(0, 1, 0) == ValueError
        assert bereken.perc_overlap(1, 0, 0) == ValueError
        assert bereken.perc_overlap(0, 0, 0) == ValueError
        assert bereken.perc_overlap(1, 1, 0) == ValueError


def test_grens():
    """Test de functie grens in bereken.py."""
    assert bereken.grens(0.025, 0, 1) == pytest.approx(-1.95996398)  # -2 SD
    assert bereken.grens(0.16, 0, 1) == pytest.approx(-0.99445788)  # -1 SD
    assert bereken.grens(0.5, 0, 1) == 0.0  # 50% dus nog op gemiddelde
    assert bereken.grens(0.84, 0, 1) == pytest.approx(0.99445788)  # 1 SD
    assert bereken.grens(0.975, 0, 1) == pytest.approx(1.95996398)  # 2 SD

    with pytest.raises(ValueError):
        assert bereken.grens(-0.5, 0, 1) == ValueError
        assert bereken.grens(0, 0, 1) == ValueError
        assert bereken.grens(1, 0, 1) == ValueError
        assert bereken.grens(1.5, 0, 1) == ValueError


def test_helling():
    """Test de functie helling in bereken.py."""
    assert bereken.helling(np.array([0, 0]), np.array([1, 0])) == 0.0
    assert bereken.helling(np.array([0, 0]), np.array([1, 1])) == 45.0
    assert bereken.helling(np.array([0, 0]), np.array([-1, -1])) == 45.0

    assert bereken.helling(np.array([0, 0]), np.array([-1, 1])) == -45.0
    assert bereken.helling(np.array([0, 0]), np.array([1, -1])) == -45.0

    assert bereken.helling(np.array([0, 0]), np.array([0, 0])) == -90
    assert bereken.helling(np.array([0, 0]), np.array([0, 1])) == -90
