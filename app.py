import streamlit as st
from datetime import datetime, date
from database import DatabaseManager
from invoice_generator.InvoicePDF import InvoicePDF  # ✅ استخدام الكلاس الجديد
from utils import get_invoice_number, validate_invoice_data
from config import INVOICES_DIR, COMPANY_NAME
import pandas as pd
import os

@st.cache_data
def get_client_names():
    with DatabaseManager() as db:
        return db.get_client_names()

if 'products' not in st.session_state:
    st.session_state.products = [{"name": "", "qty": 1, "price": 0.0, "link": ""}]

st.set_page_config(
    page_title=f"{COMPANY_NAME} Rechnung", 
    layout="wide", 
    page_icon="🧾"
)

st.title("🧾 Gesetzeskonforme Rechnungserstellung")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Kundendaten", 
    "Produkte", 
    "Einstellungen", 
    "Rechnungsarchiv",
    "Gewinnkalkulation"
])

# Tab 1: Kundendaten
with tab1:
    client_names = get_client_names()
    selected_client = st.selectbox(
        "Vorhandenen Kunden auswählen oder neuen eingeben",
        ["Neuer Kunde"] + client_names
    )

    if selected_client != "Neuer Kunde":
        with DatabaseManager() as db:
            client = db.get_client(selected_client)

        kunde_name = st.text_input("Vollständiger Name *", value=client["name"])
        email = st.text_input("E-Mail-Adresse *", value=client["email"])
        straße = st.text_input("Straße und Hausnummer *", value=client["street"])
        plz = st.text_input("Postleitzahl *", value=client["plz"])
        stadt = st.text_input("Stadt *", value=client["city"])
        land = st.text_input("Land *", value=client["country"])
    else:
        col1, col2 = st.columns(2)
        kunde_name = col1.text_input("Vollständiger Name *")
        email = col2.text_input("E-Mail-Adresse *")
        straße = col1.text_input("Straße und Hausnummer *")
        plz = col2.text_input("Postleitzahl *")
        stadt = col1.text_input("Stadt *")
        land = col2.text_input("Land *", value="Deutschland")

    delivery_date = st.date_input("Lieferdatum", value=date.today())

# Tab 2: Produkte
with tab2:
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

# Tab 3: Einstellungen
with tab3:
    mwst = st.slider("Mehrwertsteuersatz (%)", 0, 25, 19)
    hinweis = st.text_area("Zusätzliche Hinweise (optional)", value="Zahlbar innerhalb von 14 Tagen ohne Abzug.")

# Rechnung Kalkulation
netto = sum(p["qty"] * p["price"] for p in st.session_state.products if p["name"])
steuer = netto * mwst / 100
brutto = netto + steuer

st.subheader("Zusammenfassung")
col1, col2, col3 = st.columns(3)
col1.metric("Zwischensumme (Netto)", f"€{netto:.2f}")
col2.metric(f"MwSt. ({mwst}%)", f"€{steuer:.2f}")
col3.metric("Gesamtbetrag (Brutto)", f"€{brutto:.2f}")

# Button PDF erstellen
if st.button("📤 PDF-Rechnung erstellen"):
    invoice_data = {
        "rechnung_nr": get_invoice_number(),
        "datum": datetime.now().strftime("%d.%m.%Y"),
        "lief_datum": delivery_date.strftime("%d.%m.%Y"),
        "kunde_name": kunde_name,
        "email": email,
        "straße": straße,
        "plz": plz,
        "stadt": stadt,
        "land": land,
        "produkte": [p for p in st.session_state.products if p["name"]],
        "netto": float(netto),
        "steuer": float(steuer),
        "brutto": float(brutto),
        "mwst": int(mwst),
        "hinweis": hinweis
    }

    if not validate_invoice_data(invoice_data):
        st.error("Bitte überprüfen Sie alle Pflichtfelder.")
        st.stop()

    try:
        invoice_pdf = InvoicePDF()  # ✅ استخدم الكلاس الجديد
        pdf_buffer = invoice_pdf.generate(invoice_data)
        filename = f"Rechnung_{invoice_data['rechnung_nr']}.pdf"
        filepath = INVOICES_DIR / filename
        os.makedirs(INVOICES_DIR, exist_ok=True)

        with open(filepath, "wb") as f:
            f.write(pdf_buffer.getvalue())

        with DatabaseManager() as db:
            db.save_invoice({
                "invoice_no": invoice_data["rechnung_nr"],
                "client": invoice_data["kunde_name"],
                "email": invoice_data["email"],
                "date": invoice_data["datum"],
                "delivery": invoice_data["lief_datum"],
                "total": invoice_data["brutto"],
                "filename": filename
            })
            if selected_client == "Neuer Kunde":
                db.save_client({
                    "name": invoice_data["kunde_name"],
                    "email": invoice_data["email"],
                    "street": invoice_data["straße"],
                    "plz": invoice_data["plz"],
                    "city": invoice_data["stadt"],
                    "country": invoice_data["land"]
                })

        st.download_button(
            "📥 Rechnung herunterladen",
            data=pdf_buffer.getvalue(),
            file_name=filename,
            mime="application/pdf",
            key=f"dl_{invoice_data['rechnung_nr']}"
        )
        st.success(f"✅ Rechnung Nr. {invoice_data['rechnung_nr']} wurde erfolgreich erstellt.")
        st.balloons()

    except Exception as e:
        st.error(f"Fehler beim Erstellen der PDF: {str(e)}")

# Tab 4: Archiv
with tab4:
    st.subheader("🔍 Suche im Archiv")
    col1, col2 = st.columns(2)
    search_name = col1.text_input("Nach Kunde filtern")
    search_date = col2.text_input("Nach Datum (TT.MM.JJJJ) filtern")
    with DatabaseManager() as db:
        df = db.get_invoices(search_name, search_date)
    if not df.empty:
        csv = df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button("📊 Als CSV exportieren", data=csv, file_name="rechnungen_export.csv", mime="text/csv", key="csv_export")
    st.write("### Verfügbare Rechnungen")
    if df.empty:
        st.info("Keine Rechnungen gefunden.")
    else:
        for _, row in df.iterrows():
            with st.expander(f"Rechnung #{row['invoice_no']} - {row['client']} (€{row['total']:.2f})"):
                col1, col2, col3 = st.columns([1, 2, 1])
                col1.write(f"**Rechnungsnummer:** {row['invoice_no']}")
                col2.write(f"**Kunde:** {row['client']}")
                col3.write(f"**Datum:** {row['date']}")
                col1, col2 = st.columns([1, 1])
                col1.write(f"**Lieferdatum:** {row['delivery']}")
                col2.write(f"**Gesamtbetrag:** €{row['total']:.2f}")
                filepath = INVOICES_DIR / row['filename']
                if filepath.exists():
                    with open(filepath, "rb") as f:
                        st.download_button(
                            label="📄 Vollständige Rechnung herunterladen",
                            data=f.read(),
                            file_name=row['filename'],
                            mime="application/pdf",
                            key=f"dl_full_{row['invoice_no']}"
                        )
                else:
                    st.warning("PDF-Datei nicht gefunden")

# Tab 5: Gewinnkalkulation
with tab5:
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
