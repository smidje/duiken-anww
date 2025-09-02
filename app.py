import streamlit as st
import pandas as pd
from pathlib import Path
import datetime

DUIKERS_FILE = "duikers.xlsx"
PLACES_FILE = "duikplaatsen.xlsx"
DUIKEN_FILE = "duiken.xlsx"
LOGO_FILE = "logo.jpg"

def init_file(file, columns):
    path = Path(file)
    if not path.exists():
        df = pd.DataFrame(columns=columns)
        df.to_excel(file, index=False)
    return pd.read_excel(file)

def save_file(file, df):
    df.to_excel(file, index=False)

def load_duikers():
    return init_file(DUIKERS_FILE, ["Naam"])

def load_places():
    return init_file(PLACES_FILE, ["Plaats"])

def load_duiken():
    return init_file(DUIKEN_FILE, ["Datum", "Plaats", "Duiker"])

def check_login(username, password):
    return username == "admin" and password == "1234"

def login_page():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url('{LOGO_FILE}') no-repeat center center fixed;
            background-size: cover;
        }}
        .login-box {{
            background: rgba(255, 255, 255, 0.85);
            padding: 2em;
            border-radius: 15px;
            width: 300px;
            margin: auto;
            margin-top: 15%;
            text-align: center;
        }}
        </style>
        """, unsafe_allow_html=True)

    st.markdown("<div class='login-box'><h2>ANWW Duikapp Login</h2>", unsafe_allow_html=True)
    username = st.text_input("Gebruikersnaam")
    password = st.text_input("Wachtwoord", type="password", key="pw")
    if st.button("Login"):
        if check_login(username, password):
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Ongeldige login")
    st.markdown("</div>", unsafe_allow_html=True)

def header():
    st.markdown(
        f"""
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:20px;">
            <img src="{LOGO_FILE}" style="height:50px;">
            <h2 style="margin:0;">ANWW Duikapp</h2>
        </div>
        """, unsafe_allow_html=True)

def page_duiken():
    header()
    st.subheader("Nieuwe duik registreren")
    duikers_df = load_duikers()
    places_df = load_places()

    col1, col2 = st.columns(2)
    with col1:
        datum = st.date_input("Datum", datetime.date.today())
    with col2:
        plaats = st.selectbox("Duikplaats", places_df["Plaats"].tolist())

    duikers_lijst = duikers_df["Naam"].tolist()
    geselecteerde_duikers = st.multiselect("Kies duikers", duikers_lijst)

    nieuwe_duiker = st.text_input("Nieuwe duiker toevoegen")
    if st.button("Voeg nieuwe duiker toe"):
        if nieuwe_duiker and nieuwe_duiker not in duikers_lijst:
            duikers_df.loc[len(duikers_df)] = [nieuwe_duiker]
            save_file(DUIKERS_FILE, duikers_df)
            st.success(f"Duiker {nieuwe_duiker} toegevoegd.")
            st.rerun()

    if st.button("Opslaan duik(en)"):
        duiken_df = load_duiken()
        for naam in geselecteerde_duikers:
            duiken_df.loc[len(duiken_df)] = [datum, plaats, naam]
        save_file(DUIKEN_FILE, duiken_df)
        st.success("Duiken succesvol opgeslagen!")

def page_overzicht():
    header()
    st.subheader("Overzicht duiken")
    df = load_duiken()
    if df.empty:
        st.info("Nog geen duiken geregistreerd.")
    else:
        df_sorted = df.sort_values(["Datum", "Plaats"])
        st.dataframe(df_sorted, use_container_width=True)

def main():
    st.set_page_config(page_title="ANWW Duikapp", layout="wide")
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        login_page()
    else:
        tabs = st.tabs(["Duiken invoeren", "Overzicht"])
        with tabs[0]:
            page_duiken()
        with tabs[1]:
            page_overzicht()

if __name__ == "__main__":
    main()
