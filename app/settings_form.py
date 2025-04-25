import streamlit as st

class SettingsForm:
    def __init__(self):
        self.mwst = 19
        self.hinweis = "Zahlbar innerhalb von 14 Tagen ohne Abzug."

    def render(self):
        self.mwst = st.slider("Mehrwertsteuersatz (%)", 0, 25, 19)
        self.hinweis = st.text_area(
            "Zusätzliche Hinweise (optional)",
            value="Zahlbar innerhalb von 14 Tagen ohne Abzug."
        )
