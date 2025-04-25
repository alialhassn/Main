# Configuration constants
import os
from pathlib import Path

# Company Information
COMPANY_NAME = "TechFunk GmbH"
COMPANY_ADDRESS = "Innovationsstraße 12\n12345 Berlin\nDeutschland"
VAT_ID = "DE123456789"
BANK_INFO = "IBAN: DE89 3704 0044 0532 0130 00\nBIC: COBADEFFXXX\nBank: Commerzbank"
PAYMENT_TERMS = "Zahlbar innerhalb von 14 Tagen ohne Abzug."

# المسار الأساسي للمشروع (مجلد invoice_app)
BASE_DIR = Path(__file__).parent

# المسارات الأخرى
LOGO_PATH = BASE_DIR / "assets/logo.png"
FONT_REGULAR = BASE_DIR / "fonts/DejaVuSans.ttf"
FONT_BOLD = BASE_DIR / "fonts/DejaVuSans-Bold.ttf"
FONT_ITALIC = BASE_DIR / "fonts/DejaVuSans-Oblique.ttf"
INVOICE_NUMBER_FILE = BASE_DIR / "data/invoice_number.txt"
DATABASE_FILE = BASE_DIR / "data/invoices.db"
INVOICES_DIR = BASE_DIR / "invoices"

# Ensure directories exist
os.makedirs(INVOICES_DIR, exist_ok=True)
os.makedirs(BASE_DIR / "data", exist_ok=True)
os.makedirs(BASE_DIR / "assets", exist_ok=True)


# Add this to your existing config.py
#WEBSITE_URL = "https://www.youtube.com/watch?v=Xt8tdn5EcuA"  # For QR code
QR_CODE_SIZE = 30  # Size in mm
LOGO_MAX_WIDTH = 30  # Size in mm
LOGO_MAX_HEIGHT = 20  # Size in mm