import streamlit as st
from datetime import date
from database import DatabaseManager



@st.cache_data
def load_client_names():
    with DatabaseManager() as db:
        return db.get_client_names()


class ClientForm:
    def __init__(self):
        self.client_names = load_client_names()
        self.selected_client = None
        self.kunde_name = ""
        self.email = ""
        self.straße = ""
        self.plz = ""
        self.stadt = ""
        self.land = "Deutschland"
        self.delivery_date = date.today()

    @st.cache_data
    def _load_client_names(self):
        with DatabaseManager() as db:
            return db.get_client_names()

    def render(self):
        self.selected_client = st.selectbox(
            "Vorhandenen Kunden auswählen oder neuen eingeben",
            ["Neuer Kunde"] + self.client_names
        )

        if self.selected_client != "Neuer Kunde":
            with DatabaseManager() as db:
                client = db.get_client(self.selected_client)
            self.kunde_name = st.text_input("Vollständiger Name *", value=client["name"])
            self.email = st.text_input("E-Mail-Adresse *", value=client["email"])
            self.straße = st.text_input("Straße und Hausnummer *", value=client["street"])
            self.plz = st.text_input("Postleitzahl *", value=client["plz"])
            self.stadt = st.text_input("Stadt *", value=client["city"])
            self.land = st.text_input("Land *", value=client["country"])
        else:
            col1, col2 = st.columns(2)
            self.kunde_name = col1.text_input("Vollständiger Name *")
            self.email = col2.text_input("E-Mail-Adresse *")
            self.straße = col1.text_input("Straße und Hausnummer *")
            self.plz = col2.text_input("Postleitzahl *")
            self.stadt = col1.text_input("Stadt *")
            self.land = col2.text_input("Land *", value="Deutschland")

        self.delivery_date = st.date_input("Lieferdatum", value=date.today())
