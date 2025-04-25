import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st
from client_form import ClientForm
from product_form import ProductForm
from settings_form import SettingsForm
from invoice_summary import InvoiceSummary
from invoice_generator_handler import InvoiceGeneratorHandler
from invoice_archive import InvoiceArchive
from profit_calculator import ProfitCalculator


st.set_page_config(page_title="Rechnungsstellung", layout="wide")

st.title("🧾 Gesetzeskonforme Rechnungserstellung")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Kundendaten", "Produkte", "Einstellungen", "Rechnungsarchiv", "Gewinnkalkulation"
])

with tab1:
    client_form = ClientForm()
    client_form.render()

with tab2:
    product_form = ProductForm()
    product_form.render()

with tab3:
    settings_form = SettingsForm()
    settings_form.render()

    summary = InvoiceSummary(settings_form.mwst)
    summary.calculate(st.session_state.products)
    summary.render()

    generator = InvoiceGeneratorHandler(client_form, settings_form, summary)
    generator.generate_invoice()

with tab4:
    archive = InvoiceArchive()
    archive.render()

with tab5:
    profit = ProfitCalculator()
    profit.render()
