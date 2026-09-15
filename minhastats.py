# minhastats.py
import math


def media(dados):
    """Calcula a média aritmética."""
    return sum(dados) / len(dados)


def mediana(dados):
    """Calcula a mediana."""
    dados_ordenados = sorted(dados)
    n = len(dados_ordenados)
    meio = n // 2
    if n % 2 == 0:
        return (dados_ordenados[meio - 1] + dados_ordenados[meio]) / 2
    else:
        return dados_ordenados[meio]


def moda(dados):
    """Calcula a moda (pode retornar mais de um valor)."""
    frequencias = {}
    for valor in dados:
        frequencias[valor] = frequencias.get(valor, 0) + 1
    max_freq = max(frequencias.values())
    return [k for k, v in frequencias.items() if v == max_freq]


def amplitude(dados):
    """Calcula a amplitude (Max - Min)."""
    return max(dados) - min(dados)


def variancia(dados, amostral=True):
    """Calcula a variância (amostral por padrão)."""
    m = media(dados)
    soma_quadrados = sum((x - m) ** 2 for x in dados)
    denominador = len(dados) - 1 if amostral else len(dados)
    return soma_quadrados / denominador


def desvio_padrao(dados, amostral=True):
    """Calcula o desvio padrão."""
    return math.sqrt(variancia(dados, amostral))


def coeficiente_variacao(dados, amostral=True):
    """Calcula o Coeficiente de Variação (CV) em percentual."""
    return (desvio_padrao(dados, amostral) / media(dados)) * 100


def percentil(dados, p):
    """Calcula o percentil P (0 a 100)."""
    dados_ordenados = sorted(dados)
    k = (len(dados_ordenados) - 1) * (p / 100)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return dados_ordenados[int(k)]
    d0 = dados_ordenados[int(f)] * (c - k)
    d1 = dados_ordenados[int(c)] * (k - f)
    return d0 + d1


def quartis(dados):
    """Retorna Q1, Q2 (mediana) e Q3."""
    return percentil(dados, 25), mediana(dados), percentil(dados, 75)


def covariancia(x, y, amostral=True):
    """Calcula a covariância entre duas variáveis X e Y."""
    if len(x) != len(y):
        raise ValueError("As listas X e Y devem ter o mesmo tamanho.")
    media_x = media(x)
    media_y = media(y)
    soma = sum((x[i] - media_x) * (y[i] - media_y) for i in range(len(x)))
    denominador = len(x) - 1 if amostral else len(x)
    return soma / denominador


def correlacao_pearson(x, y):
    """Calcula o coeficiente de correlação de Pearson (r)."""
    cov = covariancia(x, y, amostral=True)
    dp_x = desvio_padrao(x, amostral=True)
    dp_y = desvio_padrao(y, amostral=True)
    return cov / (dp_x * dp_y)


def regressao_linear(x, y):
    """Calcula os coeficientes da regressão linear (b0, b1) e o R²."""
    cov = covariancia(x, y, amostral=True)
    var_x = variancia(x, amostral=True)
    b1 = cov / var_x
    b0 = media(y) - b1 * media(x)

    # Cálculo do R²
    y_est = [b0 + b1 * xi for xi in x]
    sq_tot = sum((yi - media(y))**2 for yi in y)
    sq_res = sum((y[i] - y_est[i])**2 for i in range(len(y)))
    r_quadrado = 1 - (sq_res / sq_tot)

    return b0, b1, r_quadrado
