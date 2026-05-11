import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_ta as ta
from concurrent.futures import ThreadPoolExecutor

# പേജ് സെറ്റിംഗ്സ്
st.set_page_config(page_title="MJ Pro Scanner Hub", layout="wide")

# സൈഡ്‌ബാർ മെനു
st.sidebar.title("📈 MJ Pro Trading Hub")
choice = st.sidebar.radio("സ്കാനർ തിരഞ്ഞെടുക്കുക:", ["Dashboard", "Breakout Scanner", "Momentum Scanner"])

# സ്കാനിംഗ് ലോജിക്
def check_breakout(ticker):
    try:
        data = yf.download(ticker, period="5d", interval="15m", progress=False)
        if data.empty: return None
        last_close = data['Close'].iloc[-1]
        prev_high = data['High'].iloc[-5:-1].max()
        if last_close > prev_high:
            return {"Ticker": ticker, "Price": round(last_close, 2), "Status": "Breakout 🚀"}
    except:
        return None

if choice == "Dashboard":
    st.title("Welcome to MJ Pro Hub")
    st.info("ഇടതുവശത്തുള്ള മെനുവിൽ നിന്ന് നിങ്ങൾക്ക് ആവശ്യമുള്ള സ്കാനർ തിരഞ്ഞെടുക്കാം.")

elif choice == "Breakout Scanner":
    st.header("🚀 Breakout Scanner Pro")
    if st.button("Scan Now"):
        stocks = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "SBIN.NS"] # കൂടുതൽ സ്റ്റോക്കുകൾ ഇവിടെ ചേർക്കാം
        with st.spinner("സ്കാൻ ചെയ്യുന്നു..."):
            with ThreadPoolExecutor(max_workers=5) as executor:
                results = list(executor.map(check_breakout, stocks))
            
            final_list = [r for r in results if r is not None]
            if final_list:
                st.table(pd.DataFrame(final_list))
            else:
                st.warning("ബ്രേക്ക്ഔട്ട് സ്റ്റോക്കുകൾ ഒന്നും കണ്ടെത്തിയില്ല.")
