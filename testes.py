# testes.py
import minhastats
import numpy as np
import statistics
import math


def test_media():
    dados = [10, 20, 30, 40, 50]
    assert math.isclose(minhastats.media(dados), np.mean(dados))


def test_variancia():
    dados = [10, 20, 30, 40, 50]
    assert math.isclose(minhastats.variancia(
        dados, amostral=True), np.var(dados, ddof=1))


def test_correlacao():
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 5, 4, 5]
    assert math.isclose(minhastats.correlacao_pearson(
        x, y), np.corrcoef(x, y)[0][1])
