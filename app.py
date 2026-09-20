import streamlit as st
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import scipy.stats as stats
import minhastats 
import math

st.set_page_config(page_title="Lab Estatístico - Games", layout="wide")
st.title("🎮 Laboratório Estatístico: Video Game Sales")

@st.cache_data
def carregar_dados():
    df = pd.read_csv("dataset/vgsales.csv")
    df = df.dropna()
    return df

df = carregar_dados()

st.header("Módulo 0: Explorando os Dados Reais")
st.dataframe(df.head())

# --------------------------------------------------------
# MÓDULO 2: ESTATÍSTICA DESCRITIVA 
# --------------------------------------------------------
st.header("Módulo 2: Estatística Descritiva")

colunas_vendas = ["NA_Sales", "EU_Sales", "JP_Sales", "Global_Sales"]
variavel_escolhida = st.selectbox("Escolha uma região para analisar as vendas:", colunas_vendas)

dados_lista = df[variavel_escolhida].tolist()

m_media = minhastats.media(dados_lista)
m_mediana = minhastats.mediana(dados_lista)
m_dp = minhastats.desvio_padrao(dados_lista)

col1, col2, col3 = st.columns(3)
col1.metric("Média", f"{m_media:.2f}")
col2.metric("Mediana", f"{m_mediana:.2f}")
col3.metric("Desvio Padrão", f"{m_dp:.2f}")


if m_media > m_mediana + (0.5 * m_dp):
    st.info("Interpretação: Assimetria à direita detectada. Valores altos (outliers) estão puxando a média para cima.")
elif m_media < m_mediana - (0.5 * m_dp):
    st.info("Interpretação: Assimetria à esquerda detectada. Valores baixos estão puxando a média para baixo.")
else:
    st.info("Interpretação: A distribuição é aproximadamente simétrica.")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

n = len(dados_lista)
k_sturges = int(1 + 3.322 * math.log10(n))
ax1.hist(dados_lista, bins=k_sturges, color='purple', edgecolor='black')
ax1.set_title(f"Histograma (Regra de Sturges: {k_sturges} classes)")


q1, q2, q3 = minhastats.quartis(dados_lista)
iqr = q3 - q1
limite_superior = q3 + 1.5 * iqr
ax2.boxplot(dados_lista, vert=False)
ax2.axvline(limite_superior, color='red', linestyle='dotted', label='Limite IQR')
ax2.set_title("Boxplot e Outliers")
ax2.legend()

st.pyplot(fig)

# --------------------------------------------------------
# MÓDULOS 3 e 4: SIMULAÇÃO E DISTRIBUIÇÕES TEÓRICAS
# --------------------------------------------------------
st.header("Módulos 3 e 4: Lei dos Grandes Números e TCL")

st.subheader("Lei dos Grandes Números (Moedas)")
lancamentos = st.slider("Número de lançamentos", 10, 5000, 100)
if st.button("Simular LGN"):
    moedas = np.random.randint(0, 2, lancamentos)
    frequencias = np.cumsum(moedas) / np.arange(1, lancamentos + 1)
    
    fig_lgn, ax_lgn = plt.subplots(figsize=(10, 3))
    ax_lgn.plot(frequencias, color='purple')
    ax_lgn.axhline(0.5, color='red', linestyle='--', label="Probabilidade Teórica (0.5)")
    ax_lgn.set_xscale('log')
    ax_lgn.set_title("Convergência da Frequência Relativa (Escala Log)")
    ax_lgn.legend()
    st.pyplot(fig_lgn)

st.subheader("Teorema Central do Limite (TCL)")
tamanho_amostra = st.slider("Tamanho da Amostra (n)", 2, 100, 30)
num_repeticoes = st.slider("Repetições", 100, 5000, 1000)

if st.button("Simular TCL"):
    medias_amostrais = [minhastats.media(np.random.choice(dados_lista, tamanho_amostra)) for _ in range(num_repeticoes)]
    
    fig_tcl, ax_tcl = plt.subplots(figsize=(10, 4))
    ax_tcl.hist(medias_amostrais, bins=40, density=True, color='dodgerblue', edgecolor='black')
    
    # Curva Teórica
    media_teorica = minhastats.media(medias_amostrais)
    dp_teorico = minhastats.desvio_padrao(medias_amostrais)
    x_eixo = np.linspace(min(medias_amostrais), max(medias_amostrais), 100)
    ax_tcl.plot(x_eixo, stats.norm.pdf(x_eixo, media_teorica, dp_teorico), 'k', linewidth=2)
    st.pyplot(fig_tcl)

# --------------------------------------------------------
# MÓDULO 5: CORRELAÇÃO E REGRESSÃO LINEAR 
# --------------------------------------------------------
st.header("Módulo 5: Regressão Linear")

col_x, col_y = st.columns(2)
with col_x:
    var_x = st.selectbox("Eixo X:", colunas_vendas, index=0)
with col_y:
    var_y = st.selectbox("Eixo Y:", colunas_vendas, index=3)

if var_x != var_y:
    x_dados = df[var_x].tolist()
    y_dados = df[var_y].tolist()
    
    correlacao = minhastats.correlacao_pearson(x_dados, y_dados)
    b0, b1, r2 = minhastats.regressao_linear(x_dados, y_dados)
    
    st.write(f"**Pearson (r):** {correlacao:.4f} | **R²:** {r2:.4f}")
    st.write(f"**Equação:** Ŷ = {b0:.4f} + {b1:.4f} * X")
    st.warning("Associação não implica causa! Cada unidade a mais de X está associada estatisticamente a mudanças em Y, mas outros fatores (como marketing) influenciam o sucesso.")

    fig3, ax3 = plt.subplots(figsize=(8, 4))
    ax3.scatter(x_dados, y_dados, alpha=0.5, color='orange')
    x_reta = [min(x_dados), max(x_dados)]
    y_reta = [b0 + b1 * x for x in x_reta]
    ax3.plot(x_reta, y_reta, color='red', linewidth=2)
    st.pyplot(fig3)

    st.subheader("🔮 Predição (Respeitando os Limites Reais)")
    min_x, max_x = min(x_dados), max(x_dados)
    
    valor_x = st.number_input(f"Digite um valor para {var_x} (entre {min_x:.2f} e {max_x:.2f}):", min_value=float(min_x), max_value=float(max_x), value=float(min_x))
    
    previsao_y = b0 + b1 * valor_x
    st.success(f"Previsão de {var_y}: **{previsao_y:.2f} milhões**")