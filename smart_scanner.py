import streamlit as st
import pandas as pd
import yfinance as yf
from concurrent.futures import ThreadPoolExecutor
import time

# --- 1. പേജ് സെറ്റിംഗ്സ് ---
st.set_page_config(page_title="MJ Pro Scanner Hub", layout="wide", page_icon="📈")

# --- 2. സ്റ്റോക്ക് ലിസ്റ്റ് (നിങ്ങൾക്ക് ഇഷ്ടമുള്ളത് ഇവിടെ ആഡ് ചെയ്യാം) ---
STOCKS = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS", 
    "SBIN.NS", "BHARTIARTL.NS", "AXISBANK.NS", "WIPRO.NS", "ITC.NS"
]

# --- 3. സ്കാനർ ലോജിക് (Functions) ---

def scan_logic(ticker, scan_type):
    try:
        df = yf.download(ticker, period="5d", interval="15m", progress=False)
        if df.empty: return None
        
        last_price = df['Close'].iloc[-1]
        prev_price = df['Close'].iloc[-2]
        high_price = df['High'].iloc[-1]
        volume = df['Volume'].iloc[-1]
        
        if scan_type == "Breakout":
            if last_price > df['High'].iloc[-5:-1].max(): # കഴിഞ്ഞ 4 കാൻഡിൽ ഹൈ ബ്രേക്ക് ചെയ്താൽ
                return {"Symbol": ticker, "LTP": round(last_price, 2), "Signal": "Breakout 🚀"}
                
        elif scan_type == "Momentum":
            change = ((last_price - prev_price) / prev_price) * 100
            if change > 0.5: # 0.5% കൂടുതൽ പെട്ടെന്ന് കയറിയാൽ
                return {"Symbol": ticker, "LTP": round(last_price, 2), "Signal": f"Up {round(change,2)}% 🔥"}
                
        return None
    except:
        return None

# --- 4. സൈഡ്‌ബാർ മെനു ---
st.sidebar.title("📈 MJ Trading Hub")
st.sidebar.write("നിങ്ങളുടെ ഓൾ-ഇൻ-വൺ സ്കാനർ")
st.sidebar.markdown("---")

menu = st.sidebar.radio("സ്കാനർ തിരഞ്ഞെടുക്കുക:", ["Dashboard", "Breakout Scanner", "Momentum Scanner"])

# --- 5. പേജ് ഡിസ്‌പ്ലേ ---

if menu == "Dashboard":
    st.title("Welcome to MJ Pro Scanner Dashboard")
    st.info("ഇടതുവശത്തുള്ള മെനുവിൽ നിന്ന് നിങ്ങൾക്ക് ആവശ്യമുള്ള സ്കാനർ തിരഞ്ഞെടുക്കുക.")
    
    col1, col2 = st.columns(2)
    col1.metric("Market Status", "Live")
    col2.metric("Active Scanners", "2")
    
    st.subheader("നിങ്ങളുടെ സ്കാനറുകൾ:")
    st.write("1. **Breakout Scanner**: റെസിസ്റ്റൻസ് ബ്രേക്ക് ചെയ്യുന്ന സ്റ്റോക്കുകൾ കണ്ടെത്താൻ.")
    st.write("2. **Momentum Scanner**: പെട്ടെന്ന് കുതിച്ചുയരുന്ന സ്റ്റോക്കുകൾ കണ്ടെത്താൻ.")

elif menu == "Breakout Scanner":
    st.header("🚀 Breakout Scanner Pro")
    if st.button("Scan for Breakouts"):
        with st.spinner("ബ്രേക്ക്ഔട്ട് സ്റ്റോക്കുകൾ കണ്ടെത്തുന്നു..."):
            with ThreadPoolExecutor(max_workers=10) as executor:
                results = list(executor.map(lambda x: scan_logic(x, "Breakout"), STOCKS))
            
            final_res = [r for r in results if r is not None]
            if final_res:
                st.table(pd.DataFrame(final_res))
            else:
                st.warning("നിലവിൽ ബ്രേക്ക്ഔട്ട് സിഗ്നലുകൾ ഒന്നുമില്ല.")

elif menu == "Momentum Scanner":
    st.header("🔥 Momentum Scanner Pro")
    if st.button("Scan for Momentum"):
        with st.spinner("മൊമെന്റം സ്റ്റോക്കുകൾ കണ്ടെത്തുന്നു..."):
            with ThreadPoolExecutor(max_workers=10) as executor:
                results = list(executor.map(lambda x: scan_logic(x, "Momentum"), STOCKS))
            
            final_res = [r for r in results if r is not None]
            if final_res:
                st.table(pd.DataFrame(final_res))
            else:
                st.warning("നിലവിൽ മൊമെന്റം സിഗ്നലുകൾ ഒന്നുമില്ല.")
