import streamlit as st

class InvoiceSummary:
    def __init__(self, mwst):
        self.mwst = mwst
        self.netto = 0.0
        self.steuer = 0.0
        self.brutto = 0.0

    def calculate(self, products):
        self.netto = sum(p["qty"] * p["price"] for p in products if p["name"])
        self.steuer = self.netto * self.mwst / 100
        self.brutto = self.netto + self.steuer

    def render(self):
        st.subheader("Zusammenfassung")
        col1, col2, col3 = st.columns(3)
        col1.metric("Zwischensumme (Netto)", f"€{self.netto:.2f}")
        col2.metric(f"MwSt. ({self.mwst}%)", f"€{self.steuer:.2f}")
        col3.metric("Gesamtbetrag (Brutto)", f"€{self.brutto:.2f}")
