import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
from datetime import datetime

# PAGE SETUP
st.set_page_config(page_title="MJ Pro Master Scanner", layout="wide")

# CSS
st.markdown("""
<style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    .card { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; text-align: center; }
    .res { color: #ff7b72; font-weight: bold; }
    .sup { color: #44cf6c; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# SIDEBAR NAVIGATION
st.sidebar.title("MJ Trading Hub")
menu = st.sidebar.radio("Navigate", ["Dashboard", "Index Scanner", "Nifty 500 Stock Scanner"])

def get_data(ticker):
    try:
        df = yf.download(ticker, period="5d", interval="15m", progress=False)
        if not df.empty:
            return df
    except: return None

# --- INDEX SCANNER ---
if menu == "Index Scanner":
    st.header("🎯 Multi-Index Pro Scanner")
    indices = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "FINNIFTY": "NIFTY_FIN_SERVICE.NS"}
    
    cols = st.columns(3)
    for i, (name, ticker) in enumerate(indices.items()):
        df = get_data(ticker)
        if df is not None:
            ltp = round(df['Close'].iloc[-1], 2)
            with cols[i]:
                st.markdown(f"""<div class='card'><h3>{name}</h3><h2>{ltp}</h2></div>""", unsafe_allow_html=True)

# --- STOCK SCANNER ---
elif menu == "Nifty 500 Stock Scanner":
    st.header("📈 Nifty 500 Momentum Scanner")
    if st.button("Start Scan"):
        # ഇവിടെ നമ്മൾ നേരത്തെ സെറ്റ് ചെയ്ത സ്റ്റോക്ക് സ്കാനിംഗ് ലോജിക് വരും
        st.info("Scanning Stocks... Please wait.")

else:
    st.title("Welcome to MJ Pro Hub")
    st.write("സ്കാനർ ഉപയോഗിക്കാൻ സൈഡ്ബാർ ഉപയോഗിക്കുക.")
