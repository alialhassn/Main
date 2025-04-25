import streamlit as st

class ProductForm:
    def __init__(self):
        if 'products' not in st.session_state:
            st.session_state.products = [{"name": "", "qty": 1, "price": 0.0, "link": ""}]

    def render(self):
        anzahl = st.number_input(
            "Anzahl der Positionen",
            min_value=1,
            max_value=20,
            value=len(st.session_state.products),
            key="product_count"
        )

        if len(st.session_state.products) != anzahl:
            diff = anzahl - len(st.session_state.products)
            if diff > 0:
                st.session_state.products.extend([{"name": "", "qty": 1, "price": 0.0, "link": ""}] * diff)
            else:
                st.session_state.products = st.session_state.products[:anzahl]

        for i in range(anzahl):
            st.markdown(f"### Position {i+1}")
            cols = st.columns([3, 1, 2])
            name = cols[0].text_input(f"Bezeichnung {i+1} *", value=st.session_state.products[i]["name"], key=f"name_{i}")
            menge = cols[1].number_input("Menge *", min_value=1, value=st.session_state.products[i]["qty"], key=f"qty_{i}")
            preis = cols[2].number_input("Einzelpreis (€) *", min_value=0.0, step=0.5, value=st.session_state.products[i]["price"], key=f"price_{i}")
            link = st.text_input(f"Produktlink {i+1} (optional)", value=st.session_state.products[i].get("link", ""), key=f"link_{i}")
            st.session_state.products[i] = {"name": name, "qty": menge, "price": preis, "link": link}
