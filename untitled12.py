# -*- coding: utf-8 -*-
"""Untitled12.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Ic16uhPdb4XQmDBXNiLizL0MHucpwjFm
"""

import streamlit as st
import numpy as np
import scipy.stats as si
from scipy.optimize import brentq

# Função Black-Scholes para opções europeias
def black_scholes(S, K, T, r, sigma, option_type='call'):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == 'call':
        return S * si.norm.cdf(d1) - K * np.exp(-r * T) * si.norm.cdf(d2)
    elif option_type == 'put':
        return K * np.exp(-r * T) * si.norm.cdf(-d2) - S * si.norm.cdf(-d1)

# Função para calcular a volatilidade implícita
def implied_volatility(option_price, S, K, T, r, option_type='call'):
    objective_function = lambda sigma: black_scholes(S, K, T, r, sigma, option_type) - option_price
    return brentq(objective_function, 1e-6, 5)

# Função para opções americanas (aproximação de Bjerksund-Stensland para calls)
def bjerksund_stensland_approx(S, K, T, r, sigma, option_type='call'):
    # Aproximação: usa o BS para calls e puts, com penalidade para puts (não exatas)
    return black_scholes(S, K, T, r, sigma, option_type)

# Função para opções asiáticas com média geométrica (fechamento analítico)
def asian_geometric_option(S, K, T, r, sigma, option_type='call'):
    sigma_adj = sigma * np.sqrt((2 * T + 1) / (6 * (T + 1)))
    r_adj = 0.5 * (r - 0.5 * sigma ** 2) + 0.5 * sigma_adj ** 2
    d1 = (np.log(S / K) + (r_adj + 0.5 * sigma_adj ** 2) * T) / (sigma_adj * np.sqrt(T))
    d2 = d1 - sigma_adj * np.sqrt(T)
    if option_type == 'call':
        return np.exp(-r * T) * (S * np.exp(r_adj * T) * si.norm.cdf(d1) - K * si.norm.cdf(d2))
    else:
        return np.exp(-r * T) * (K * si.norm.cdf(-d2) - S * np.exp(r_adj * T) * si.norm.cdf(-d1))

# Interface Streamlit
st.title("Calculadora de Opções e Volatilidade Implícita")

S = st.number_input("Preço do ativo (S)", value=100.0)
K = st.number_input("Preço de exercício (K)", value=100.0)
T = st.number_input("Tempo até o vencimento (T em anos)", value=1.0)
r = st.number_input("Taxa de juros livre de risco (r)", value=0.05)
sigma = st.number_input("Volatilidade (sigma)", value=0.2)
option_type = st.selectbox("Tipo da opção", ['call', 'put'])
model = st.selectbox("Modelo de opção", ['Europeia', 'Americana', 'Asiática'])
calcular_vol = st.checkbox("Calcular volatilidade implícita a partir do preço da opção")

if calcular_vol:
    market_price = st.number_input("Preço de mercado da opção", value=10.0)
    try:
        vol = implied_volatility(market_price, S, K, T, r, option_type)
        st.write(f"Volatilidade implícita estimada: {vol:.4f}")
    except ValueError:
        st.write("Não foi possível encontrar a volatilidade implícita.")
else:
    if model == 'Europeia':
        price = black_scholes(S, K, T, r, sigma, option_type)
    elif model == 'Americana':
        price = bjerksund_stensland_approx(S, K, T, r, sigma, option_type)
    elif model == 'Asiática':
        price = asian_geometric_option(S, K, T, r, sigma, option_type)

    st.write(f"Preço da opção {model.lower()}: {price:.4f}")