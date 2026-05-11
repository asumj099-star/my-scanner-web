import streamlit as st
import pandas as pd
import yfinance as yf
from concurrent.futures import ThreadPoolExecutor

# --- 1. പേജ് സെറ്റിംഗ്സ് ---
st.set_page_config(page_title="MJ Pro Scanner Hub", layout="wide", page_icon="📈")

# --- 2. സ്റ്റോക്ക് ലിസ്റ്റ് (ഇവിടെ നിങ്ങൾക്ക് കൂടുതൽ സ്റ്റോക്കുകൾ ആഡ് ചെയ്യാം) ---
STOCKS = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS", 
    "SBIN.NS", "BHARTIARTL.NS", "AXISBANK.NS", "WIPRO.NS", "ITC.NS",
    "TATAMOTORS.NS", "ADANIENT.NS", "BAJFINANCE.NS", "LT.NS", "M&M.NS",
    "TITAN.NS", "SUNPHARMA.NS", "ULTRACEMCO.NS", "ASIANPAINT.NS", "KOTAKBANK.NS"
]

# --- 3. സ്കാനർ എൻജിൻ (എല്ലാ കണ്ടീഷനുകളും ഇവിടെയുണ്ട്) ---
def advanced_scan(ticker):
    try:
        # 15 മിനിറ്റ് ഇന്റർവെലിൽ ഡാറ്റ എടുക്കുന്നു
        df = yf.download(ticker, period="5d", interval="15m", progress=False)
        if df.empty or len(df) < 20: return None
        
        last_close = df['Close'].iloc[-1]
        prev_close = df['Close'].iloc[-2]
        high_5 = df['High'].iloc[-6:-1].max() # കഴിഞ്ഞ 5 കാൻഡിലുകളിലെ ഹൈ
        avg_vol = df['Volume'].iloc[-10:-1].mean()
        curr_vol = df['Volume'].iloc[-1]
        
        results = {"Symbol": ticker, "LTP": round(last_close, 2)}
        
        # A. Breakout Logic
        if last_close > high_5:
            results["Breakout"] = "🚀 Breakout"
        else:
            results["Breakout"] = "-"

        # B. Momentum Logic (0.3% കൂടുതൽ മൂവ്‌മെന്റ്)
        change = ((last_price - prev_close) / prev_close) * 100
        if change > 0.3:
            results["Momentum"] = f"🔥 Bullish ({round(change,2)}%)"
        elif change < -0.3:
            results["Momentum"] = f"❄️ Bearish ({round(change,2)}%)"
        else:
            results["Momentum"] = "Neutral"

        # C. Volume Spike
        if curr_vol > avg_vol * 1.5:
            results["Volume"] = "✅ High Vol"
        else:
            results["Volume"] = "Normal"

        return results
    except:
        return None

# --- 4. സൈഡ്‌ബാർ മെനു ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2422/2422796.png", width=100)
st.sidebar.title("MJ Trading Hub")
st.sidebar.markdown("---")
menu = st.sidebar.radio("മെനു തിരഞ്ഞെടുക്കുക:", ["🏠 Dashboard", "🔍 Multi-Scanner Pro", "📊 Market Watch"])

# --- 5. പേജ് ലോജിക് ---

if menu == "🏠 Dashboard":
    st.title("Welcome to MJ Pro Trading Hub")
    st.info("നിങ്ങളുടെ സ്കാനറുകൾ ഇപ്പോൾ ലൈവ് ആണ്. ഇടതുവശത്തെ മെനുവിൽ നിന്ന് സ്കാനർ സെലക്ട് ചെയ്യുക.")
    
    # സ്റ്റാറ്റസ് ബോക്സുകൾ
    c1, c2, c3 = st.columns(3)
    c1.metric("Market", "NSE/BSE")
    c2.metric("Scanners", "Active")
    c3.metric("Version", "2.0")

elif menu == "🔍 Multi-Scanner Pro":
    st.header("🚀 All-in-One Multi Scanner")
    st.write("ഈ സ്കാനർ ഒരേസമയം Breakout, Momentum, Volume എന്നിവ പരിശോധിക്കും.")
    
    if st.button("Start Full Scan"):
        with st.spinner("നിങ്ങളുടെ സ്കാനർ സ്റ്റോക്കുകൾ പരിശോധിക്കുന്നു..."):
            with ThreadPoolExecutor(max_workers=10) as executor:
                raw_results = list(executor.map(advanced_scan, STOCKS))
            
            # ഫിൽട്ടറിംഗ്
            final_data = [r for r in raw_results if r is not None]
            
            if final_data:
                df_final = pd.DataFrame(final_data)
                # ലിസ്റ്റ് കാണിക്കുന്നു
                st.dataframe(df_final.style.highlight_max(axis=0, color='#1e40af'), use_container_width=True)
                st.success(f"സ്കാനിംഗ് പൂർത്തിയായി. {len(final_data)} സ്റ്റോക്കുകൾ കണ്ടെത്തി.")
            else:
                st.error("ഡാറ്റ ലഭ്യമല്ല. ദയവായി അല്പം കഴിഞ്ഞ് ശ്രമിക്കുക.")

elif menu == "📊 Market Watch":
    st.header("Market Overview")
    st.write("പ്രധാന ഇൻഡക്സുകൾ ഇവിടെ നിരീക്ഷിക്കാം (Coming Soon).")
