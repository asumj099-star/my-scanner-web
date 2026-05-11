import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
from datetime import datetime
import time

# --- 1. പേജ് സെറ്റിംഗ്സ് ---
st.set_page_config(page_title="MJ Pro Master Hub", layout="wide", page_icon="🎯")

# --- 2. CSS STYLING (എല്ലാ സ്കാനറുകൾക്കും വേണ്ടിയുള്ള കോമൺ സ്റ്റൈൽ) ---
st.markdown("""
<style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    .card { background-color: #161b22; padding: 15px; border-radius: 12px; border: 1px solid #30363d; text-align: center; margin-bottom: 10px; }
    .top-bar { display: flex; justify-content: space-around; background: #1f2937; padding: 10px; border-radius: 10px; margin-bottom: 15px; border: 1px solid #3b82f6; align-items: center; }
    .levels-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 4px; margin: 8px 0; font-size: 10px; }
    .res { color: #ff7b72; font-weight: bold; }
    .sup { color: #44cf6c; font-weight: bold; }
    .strike-table { width: 100%; font-size: 11px; border-collapse: collapse; margin-top: 8px; border-radius: 5px; overflow: hidden; }
    .strike-table td { padding: 5px; border: 1px solid #30363d; text-align: center; }
    .itm { background-color: #1c2a1e; color: #44cf6c; }
    .atm { background-color: #262c36; color: #ffab70; font-weight: bold; }
    .otm { color: #8b949e; }
    .heatmap-container { background: #0d1117; padding: 15px; border-radius: 12px; border: 1px solid #333; }
    .stock-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(85px, 1fr)); gap: 5px; }
    .stock-box { padding: 8px 4px; border-radius: 6px; font-size: 10px; font-weight: bold; text-align: center; border: 1px solid #222; }
    .pos { background-color: #1c2a1e; color: #44cf6c; border-color: #44cf6c; }
    .neg { background-color: #2a1c1c; color: #ff7b72; border-color: #ff7b72; }
    .stat-box { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; text-align: center; color: white; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

# --- 3. COMMON FUNCTIONS ---
def get_index_data(ticker):
    try:
        data = yf.download(ticker, period="2d", interval="15m", progress=False)
        if not data.empty:
            if isinstance(data.columns, pd.MultiIndex): data.columns = data.columns.get_level_values(0)
            h, l, c = data['High'].iloc[-2], data['Low'].iloc[-2], data['Close'].iloc[-2]
            p = (h + l + c) / 3
            curr = data['Close'].iloc[-1]
            return {"curr": round(float(curr), 2), "R1": round(2*p-l, 2), "S1": round(2*p-h, 2), "R2": round(p+(h-l), 2), "S2": round(p-(h-l), 2)}
    except: return None

def get_option_chain_html(price, base=50):
    atm = round(price / base) * base
    html = "<table class='strike-table'>"
    for i in range(-1, 2):
        s = int(atm + (i * base))
        style = "itm" if s < atm else "atm" if s == atm else "otm"
        html += f"<tr class='{style}'><td>{s}</td></tr>"
    return html + "</table>"

# --- 4. SIDEBAR NAVIGATION ---
st.sidebar.title("MJ Trading Hub Pro")
page = st.sidebar.radio("സ്കാനർ തിരഞ്ഞെടുക്കുക:", ["🏠 Dashboard", "🎯 Multi-Index Pro", "💎 Option Pro", "📈 Stock Pro (Nifty 500)"])

# --- 5. DASHBOARD PAGE ---
if page == "🏠 Dashboard":
    st.title("MJ Pro Scanner Dashboard")
    st.write("സ്കാനറുകൾ പ്രവർത്തിപ്പിക്കാൻ സൈഡ്ബാർ മെനു ഉപയോഗിക്കുക.")
    col1, col2 = st.columns(2)
    with col1:
        st.info("Market Status: Live Update Enabled")
    with col2:
        st.success(f"Last Login: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# --- 6. MULTI-INDEX PRO PAGE ---
elif page == "🎯 Multi-Index Pro":
    st.header("Multi-Index Master Scanner")
    indices = [("^NSEI", "NIFTY 50"), ("^NSEBANK", "BANK NIFTY"), ("NIFTY_FIN_SERVICE.NS", "FINNIFTY")]
    cols = st.columns(3)
    for i, (tic, name) in enumerate(indices):
        data = get_index_data(tic)
        if data:
            with cols[i]:
                st.markdown(f"""<div class="card"><h4>{name}</h4><h2>{data['curr']}</h2><div class="levels-grid">
                <span class="res">R1: {data['R1']}</span><span class="sup">S1: {data['S1']}</span></div>
                {get_option_chain_html(data['curr'])}</div>""", unsafe_allow_html=True)

# --- 7. OPTION PRO PAGE ---
elif page == "💎 Option Pro":
    st.header("Ultimate Option Pro Scanner")
    nifty = get_index_data("^NSEI")
    if nifty:
        st.markdown(f"""<div class="card" style="max-width:400px; margin:auto;"><h3>NIFTY 50 SPOT</h3><h1>{nifty['curr']}</h1>
        {get_option_chain_html(nifty['curr'], 50)}</div>""", unsafe_allow_html=True)

# --- 8. STOCK PRO PAGE ---
elif page == "📈 Stock Pro (Nifty 500)":
    st.header("Nifty 500 Advanced Scanner")
    if st.button("🚀 START MARKET SCAN"):
        st.warning("സ്കാനിംഗ് ആരംഭിക്കുന്നു... ദയവായി കാത്തിരിക്കുക.")
        # ഇവിടെ നിങ്ങൾക്ക് സ്റ്റോക്ക് സ്കാനിംഗ് ലോജിക് ചേർക്കാം
        st.info("നിങ്ങൾ നൽകിയ Nifty 500 ലിസ്റ്റിലെ സ്റ്റോക്കുകൾ ഇവിടെ സ്കാൻ ചെയ്യപ്പെടും.")

st.sidebar.markdown("---")
st.sidebar.caption(f"Last Update: {datetime.now().strftime('%H:%M:%S')}")
