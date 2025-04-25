import os
from config import COMPANY_NAME, LOGO_PATH

class InvoiceHeader:
    def __init__(self, pdf):
        self.pdf = pdf

    def add(self, invoice_data):
        # إضافة الشعار
        if os.path.exists(LOGO_PATH):
            try:
                self.pdf.image(LOGO_PATH, x=10, y=8, w=40)
            except Exception as e:
                print(f"Logo loading failed: {e}")

        # عنوان الفاتورة
        self.pdf.set_font("DejaVu", "B", 20)
        self.pdf.set_text_color(44, 62, 80)
        self.pdf.set_xy(0, 12)
        self.pdf.cell(0, 10, "RECHNUNG", ln=True, align="C")

        # تفاصيل الفاتورة
        self.pdf.set_font("DejaVu", "", 10)
        self.pdf.set_text_color(100, 100, 100)
        self.pdf.set_xy(0, 22)
        self.pdf.cell(0, 6, f"Nr. {invoice_data.get('rechnung_nr')}", ln=True, align="C")
        self.pdf.cell(0, 6, f"vom {invoice_data.get('datum')}", ln=True, align="C")

        self.pdf.set_line_width(0.5)
        self.pdf.set_draw_color(200, 200, 200)
        self.pdf.line(10, 35, 200, 35)
        self.pdf.ln(15)
