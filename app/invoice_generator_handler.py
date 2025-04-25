import os
import streamlit as st
from datetime import datetime
from database import DatabaseManager
from utils import get_invoice_number, validate_invoice_data
from config import INVOICES_DIR
from invoice_generator.InvoicePDF import InvoicePDF

class InvoiceGeneratorHandler:
    def __init__(self, client_form, settings_form, summary):
        self.client_form = client_form
        self.settings_form = settings_form
        self.summary = summary

    def generate_invoice(self):
        if "pdf_generated" not in st.session_state:
            st.session_state.pdf_generated = False
            st.session_state.pdf_filename = ""
            st.session_state.pdf_buffer = None

        if st.button("📤 Rechnung erstellen"):
            invoice_data = {
                "rechnung_nr": get_invoice_number(),
                "datum": datetime.now().strftime("%d.%m.%Y"),
                "lief_datum": self.client_form.delivery_date.strftime("%d.%m.%Y"),
                "kunde_name": self.client_form.kunde_name,
                "email": self.client_form.email,
                "straße": self.client_form.straße,
                "plz": self.client_form.plz,
                "stadt": self.client_form.stadt,
                "land": self.client_form.land,
                "produkte": [p for p in st.session_state.products if p["name"]],
                "netto": float(self.summary.netto),
                "steuer": float(self.summary.steuer),
                "brutto": float(self.summary.brutto),
                "mwst": int(self.settings_form.mwst),
                "hinweis": self.settings_form.hinweis
            }

            if not validate_invoice_data(invoice_data):
                st.error("Bitte überprüfen Sie alle Pflichtfelder.")
                st.stop()

            try:
                invoice_pdf = InvoicePDF()
                pdf_buffer = invoice_pdf.generate(invoice_data)
                filename = f"Rechnung_{invoice_data['rechnung_nr']}.pdf"
                filepath = INVOICES_DIR / filename
                os.makedirs(INVOICES_DIR, exist_ok=True)

                with open(filepath, "wb") as f:
                    f.write(pdf_buffer.getvalue())

                # حفظ حالة الإنشاء في السيشن
                st.session_state.pdf_generated = True
                st.session_state.pdf_filename = filename
                st.session_state.pdf_buffer = pdf_buffer

                # حفظ في قاعدة البيانات
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
                    if self.client_form.selected_client == "Neuer Kunde":
                        db.save_client({
                            "name": invoice_data["kunde_name"],
                            "email": invoice_data["email"],
                            "street": invoice_data["straße"],
                            "plz": invoice_data["plz"],
                            "city": invoice_data["stadt"],
                            "country": invoice_data["land"]
                        })

                st.success(f"✅ Rechnung Nr. {invoice_data['rechnung_nr']} wurde erfolgreich erstellt.")
                st.balloons()

            except Exception as e:
                st.error(f"Fehler beim Erstellen der PDF: {str(e)}")

        # ✅ زر تحميل الفاتورة إذا كانت جاهزة
        if st.session_state.pdf_generated and st.session_state.pdf_buffer:
            st.download_button(
                "📥 Rechnung herunterladen",
                data=st.session_state.pdf_buffer.getvalue(),
                file_name=st.session_state.pdf_filename,
                mime="application/pdf",
                key="download_invoice_btn"
            )
