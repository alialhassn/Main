import streamlit as st

class ProfitCalculator:
    def render(self):
        st.subheader("📈 Gewinnkalkulation (Profit Calculation)")

        einkaufspreis = st.number_input("Einkaufspreis (€)", min_value=0.0, value=0.0, step=0.5)
        marge = st.slider("Gewünschte Gewinnmarge (%)", min_value=30, max_value=50, value=40)
        versandkosten = st.number_input("Versandkosten (€)", min_value=0.0, value=0.0, step=0.5)

        if einkaufspreis > 0:
            nettowert = einkaufspreis * (1 + marge / 100)
            mehrwertsteuer = nettowert * 0.19
            endpreis = nettowert + mehrwertsteuer + versandkosten

            st.metric("Nettoverkaufspreis", f"€{nettowert:.2f}")
            st.metric("Mehrwertsteuer (19%)", f"€{mehrwertsteuer:.2f}")
            st.metric("Endpreis (inkl. MwSt. und Versand)", f"€{endpreis:.2f}")
        else:
            st.info("Bitte geben Sie den Einkaufspreis ein.")
