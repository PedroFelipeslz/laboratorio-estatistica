import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import minhastats


st.set_page_config(page_title="Lab Estatístico - Games", layout="wide")
st.title("Laboratório Estatístico: Video Game Sales")


@st.cache_data
def carregar_dados():
    # Lê o arquivo CSV lá daquela pastinha que criamos
    df = pd.read_csv("dataset/vgsales.csv")
    # Limpa linhas vazias para não quebrar a nossa matemática
    df = df.dropna()
    return df


df = carregar_dados()

st.header("Módulo 0: Explorando os Dados Reais")
st.write("Abaixo está uma amostra do nosso dataset de vendas de jogos (em milhões de unidades):")
st.dataframe(df.head(10))

st.header("Módulo 2: Estatística Descritiva")


colunas_vendas = ["NA_Sales", "EU_Sales", "JP_Sales", "Global_Sales"]
variavel_escolhida = st.selectbox(
    "Escolha uma região para analisar as vendas:", colunas_vendas)


dados_lista = df[variavel_escolhida].tolist()

st.subheader(
    f"Medidas calculadas pela biblioteca própria (minhastats.py) para {variavel_escolhida}")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Média", f"{minhastats.media(dados_lista):.2f}")
    st.metric("Mediana", f"{minhastats.mediana(dados_lista):.2f}")

with col2:
    st.metric("Amplitude", f"{minhastats.amplitude(dados_lista):.2f}")
    st.metric("Variância", f"{minhastats.variancia(dados_lista):.2f}")

with col3:
    st.metric("Desvio Padrão", f"{minhastats.desvio_padrao(dados_lista):.2f}")
    st.metric("Coef. de Variação",
              f"{minhastats.coeficiente_variacao(dados_lista):.2f}%")


st.write("**Histograma de Frequência**")
fig, ax = plt.subplots(figsize=(10, 4))
ax.hist(dados_lista, bins=50, color='purple', edgecolor='black',
        range=(0, 2))  # Limitado a 2 milhões para visualizar melhor
ax.set_title(f"Distribuição de {variavel_escolhida}")
st.pyplot(fig)

st.header("Módulos 3 e 4: Monte Carlo e Teorema Central do Limite")
st.write("Vamos simular a coleta de amostras aleatórias das vendas de jogos. Mesmo que a distribuição original não seja simétrica, a média dessas amostras deve formar uma Curva Normal (Sino) perfeita!")


col_param1, col_param2 = st.columns(2)
with col_param1:
    tamanho_amostra = st.slider(
        "Tamanho da Amostra (n)", min_value=10, max_value=500, value=30)
with col_param2:
    num_repeticoes = st.slider(
        "Número de Repetições", min_value=100, max_value=5000, value=1000)

if st.button("Rodar Simulação"):
    import random
    import numpy as np
    import scipy.stats as stats

    medias_amostrais = []

    for _ in range(num_repeticoes):
        amostra = random.choices(dados_lista, k=tamanho_amostra)
        medias_amostrais.append(minhastats.media(amostra))

    fig2, ax2 = plt.subplots(figsize=(10, 4))

    ax2.hist(medias_amostrais, bins=40, density=True, alpha=0.6,
             color='dodgerblue', edgecolor='black', label="Médias Amostrais")

    media_teorica = minhastats.media(medias_amostrais)
    dp_teorico = minhastats.desvio_padrao(medias_amostrais)
    xmin, xmax = ax2.get_xlim()
    eixo_x = np.linspace(xmin, xmax, 100)
    curva_normal = stats.norm.pdf(eixo_x, media_teorica, dp_teorico)

    ax2.plot(eixo_x, curva_normal, 'k', linewidth=2,
             label="Curva Normal Teórica")
    ax2.set_title(f"Distribuição das Médias - {variavel_escolhida}")
    ax2.legend()
    st.pyplot(fig2)

st.header("Módulo 5: Regressão Linear e Predição")
st.write("Será que as vendas de uma região servem para prever as vendas de outra?")

col_x, col_y = st.columns(2)
with col_x:
    var_x = st.selectbox("Variável Independente (X):",
                         colunas_vendas, index=0)  # Padrão: NA_Sales
with col_y:
    var_y = st.selectbox("Variável Dependente (Y):",
                         colunas_vendas, index=3)   # Padrão: Global_Sales

if var_x != var_y:
    # Pegando os dados das colunas escolhidas
    x_dados = df[var_x].tolist()
    y_dados = df[var_y].tolist()

    # Cálculos matemáticos usando nossa biblioteca minhastats.py
    correlacao = minhastats.correlacao_pearson(x_dados, y_dados)
    b0, b1, r2 = minhastats.regressao_linear(x_dados, y_dados)

    st.write(f"**Correlação de Pearson (r):** {correlacao:.4f}")
    st.write(f"**Coeficiente de Determinação (R²):** {r2:.4f}")
    st.write(f"**Equação da Reta:** Ŷ = {b0:.4f} + {b1:.4f} * X")
    st.warning("🚨 Alerta de Integridade Estatística: Correlação forte não implica causalidade! Um jogo vender bem no mundo não é 'causado' apenas por ele ter vendido bem em uma região específica.")

    # Gráfico de Dispersão com a Reta de Regressão
    fig3, ax3 = plt.subplots(figsize=(8, 4))
    ax3.scatter(x_dados, y_dados, alpha=0.5,
                color='orange', label="Jogos (Dados Reais)")

    # Desenhando a reta matemática na unha
    x_min, x_max = min(x_dados), max(x_dados)
    x_reta = [x_min, x_max]
    y_reta = [b0 + b1 * x for x in x_reta]
    ax3.plot(x_reta, y_reta, color='red',
             linewidth=2, label="Reta de Regressão")

    ax3.set_xlabel(f"Vendas em {var_x}")
    ax3.set_ylabel(f"Vendas em {var_y}")
    ax3.legend()
    st.pyplot(fig3)

    # Ferramenta de Predição Interativa
    st.subheader("🔮 Predição Interativa")
    valor_x = st.number_input(
        f"Digite um valor hipotético de vendas para {var_x} (em milhões):", value=1.0)
    previsao_y = b0 + b1 * valor_x
    st.success(
        f"O nosso modelo estatístico prevê que as vendas de {var_y} seriam de aproximadamente **{previsao_y:.2f} milhões**!")
else:
    st.error(
        "Por favor, escolha variáveis diferentes para X e Y para calcular a correlação.")
