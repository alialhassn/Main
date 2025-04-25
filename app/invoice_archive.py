import streamlit as st
import pandas as pd
from database import DatabaseManager
from config import INVOICES_DIR

class InvoiceArchive:
    def render(self):
        st.subheader("🔍 Suche im Archiv")
        col1, col2 = st.columns(2)
        search_name = col1.text_input("Nach Kunde filtern")
        search_date = col2.text_input("Nach Datum (TT.MM.JJJJ) filtern")

        with DatabaseManager() as db:
            df = db.get_invoices(search_name, search_date)

        if not df.empty:
            csv = df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                "📊 Als CSV exportieren",
                data=csv,
                file_name="rechnungen_export.csv",
                mime="text/csv",
                key="csv_export"
            )
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
