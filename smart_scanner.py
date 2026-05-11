import streamlit as st

# പേജ് ഡിസൈൻ
st.set_page_config(page_title="MJ Multi-Scanner Hub", layout="wide")

# സൈഡ്‌ബാർ മെനു
st.sidebar.title("MJ Trading Hub")
selection = st.sidebar.radio("സ്കാനർ തിരഞ്ഞെടുക്കുക:", ["Dashboard", "Breakout Scanner", "Momentum Scanner"])

if selection == "Dashboard":
    st.title("Welcome to MJ Scanner Hub")
    st.write("ഇടതുവശത്തെ മെനുവിൽ നിന്ന് സ്കാനർ തിരഞ്ഞെടുക്കുക.")

elif selection == "Breakout Scanner":
    # നിങ്ങളുടെ നിലവിലുള്ള സ്കാനർ കോഡ് ഇവിടെ പേസ്റ്റ് ചെയ്യുക
    st.header("Breakout Scanner Active")
    
elif selection == "Momentum Scanner":
    # നിങ്ങളുടെ രണ്ടാമത്തെ സ്കാനർ കോഡ് ഇവിടെ പേസ്റ്റ് ചെയ്യുക
    st.header("Momentum Scanner Active")
