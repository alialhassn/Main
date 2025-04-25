from config import BANK_INFO, PAYMENT_TERMS, COMPANY_NAME
from invoice_generator.ProductQRGenerator import ProductQRGenerator
import os

class InvoiceFooter:
    def __init__(self, pdf):
        self.pdf = pdf

    def add(self, invoice_data):
        self.pdf.set_font("DejaVu", "B", 10)
        self.pdf.cell(0, 7, "ZAHLUNGSBEDINGUNGEN:", ln=True)
        self.pdf.set_font("DejaVu", "", 9)
        self.pdf.multi_cell(100, 5, invoice_data.get('hinweis', PAYMENT_TERMS))
        self.pdf.ln(5)

        self.pdf.set_font("DejaVu", "B", 10)
        self.pdf.cell(0, 7, "ZAHLUNGSWEG:", ln=True)
        self.pdf.set_font("DejaVu", "", 9)
        self.pdf.multi_cell(100, 5, BANK_INFO)

        # ✅ إضافة QR من أول منتج
        first_product_with_link = next((p for p in invoice_data.get('produkte', []) if p.get('link')), None)
        if first_product_with_link:
            qr_path = ProductQRGenerator.generate_qr(first_product_with_link["link"])
            if qr_path and os.path.exists(qr_path):
                try:
                    self.pdf.set_xy(self.pdf.w/2, self.pdf.get_y()-40)
                    self.pdf.image(qr_path, x=self.pdf.w-40, y=self.pdf.get_y(), w=25)
                    os.unlink(qr_path)
                except Exception as e:
                    print(f"QR code placement failed: {e}")

        self.pdf.set_y(-20)
        self.pdf.set_font("DejaVu", "I", 8)
        self.pdf.set_text_color(150, 150, 150)
        self.pdf.cell(0, 5, "Vielen Dank für Ihren Auftrag!", ln=True, align="C")
        self.pdf.cell(0, 5, COMPANY_NAME, ln=True, align="C")
