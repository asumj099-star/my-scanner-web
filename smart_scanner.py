import streamlit as st
import pandas as pd
import yfinance as yf
from concurrent.futures import ThreadPoolExecutor

# --- 1. പേജ് സെറ്റിംഗ്സ് ---
st.set_page_config(page_title="MJ Trading Hub Scanner", layout="wide")

# --- 2. സ്റ്റോക്ക് ലിസ്റ്റ് (നിങ്ങളുടെ താല്പര്യപ്രകാരം മാറ്റാം) ---
NIFTY50_TICKERS = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "BHARTIARTL.NS"]

# --- 3. സ്കാനർ ലോജിക് ഫംഗ്ഷനുകൾ ---

def analyze_stock(ticker):
    """ഒരു സ്റ്റോക്ക് അനലൈസ് ചെയ്യാനുള്ള ലോജിക്"""
    try:
        data = yf.download(ticker, period="5d", interval="15m", progress=False)
        if data.empty: return None
        
        last_close = data['Close'].iloc[-1]
        prev_close = data['Close'].iloc[-2]
        
        # ഉദാഹരണത്തിന് ഒരു സിമ്പിൾ ബ്രേക്ക്ഔട്ട് കണ്ടീഷൻ
        if last_close > prev_close * 1.01: # 1% കയറിയാൽ
            return {"Ticker": ticker, "LTP": round(last_close, 2), "Change": "Breakout"}
        return None
    except:
        return None

# --- 4. സൈഡ്‌ബാർ മെനു ---
st.sidebar.title("📈 MJ Pro Scanner")
choice = st.sidebar.radio("സ്കാനർ തിരഞ്ഞെടുക്കുക:", ["Home", "Breakout Scanner", "Momentum Scanner"])

# --- 5. പേജ് ഡിസ്‌പ്ലേ ലോജിക് ---

if choice == "Home":
    st.title("Welcome to MJ Trading Hub")
    st.write("ഇടതുവശത്തുള്ള മെനുവിൽ നിന്ന് സ്കാനർ സെലക്ട് ചെയ്യുക.")

elif choice == "Breakout Scanner":
    st.header("🚀 Breakout Scanner Pro")
    
    if st.button("Scan Now"):
        with st.spinner("സ്റ്റോക്കുകൾ സ്കാൻ ചെയ്യുന്നു..."):
            with ThreadPoolExecutor(max_workers=10) as executor:
                results = list(executor.map(analyze_stock, NIFTY50_TICKERS))
            
            # ഫിൽട്ടർ ചെയ്ത റിസൾട്ടുകൾ കാണിക്കുന്നു
            final_list = [r for r in results if r is not None]
            
            if final_list:
                df = pd.DataFrame(final_list)
                st.table(df) # ഇവിടെയാണ് ടേബിൾ രൂപത്തിൽ റിസൾട്ട് വരുന്നത്
            else:
                st.warning("നിലവിൽ ബ്രേക്ക്ഔട്ട് കണ്ടീഷനിൽ സ്റ്റോക്കുകൾ ഒന്നുമില്ല.")

elif choice == "Momentum Scanner":
    st.header("🔥 Momentum Scanner")
    st.write("മൊമെന്റം സ്കാനർ റിസൾട്ടുകൾ ഇവിടെ വരും.")
