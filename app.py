import streamlit as st
import pandas as pd
import ta

st.title("Analisador de Mercado — M1")

uploaded = st.file_uploader("Envie CSV de candles", type=['csv'])
if uploaded:
    df = pd.read_csv(uploaded)
    df['ema20'] = df['close'].ewm(span=20).mean()
    df['ema50'] = df['close'].ewm(span=50).mean()
    df['rsi14'] = ta.momentum.RSIIndicator(df['close'], 14).rsi()

    sinal = []
    for i in range(len(df)):
        if df['ema20'].iloc[i] > df['ema50'].iloc[i] and df['rsi14'].iloc[i] > 50:
            sinal.append("CALL")
        elif df['ema20'].iloc[i] < df['ema50'].iloc[i] and df['rsi14'].iloc[i] < 50:
            sinal.append("PUT")
        else:
            sinal.append("AGUARDAR")

    df['sinal'] = sinal
    st.dataframe(df.tail(20))
    st.write("Contagem de sinais:", df['sinal'].value_counts())
