class InvoiceProductTable:
    def __init__(self, pdf):
        self.pdf = pdf

    def add(self, invoice_data):
        self.pdf.set_fill_color(44, 62, 80)
        self.pdf.set_text_color(255, 255, 255)
        self.pdf.set_font("DejaVu", "B", 9)

        self.pdf.cell(90, 8, "BESCHREIBUNG", border=1, fill=True)
        self.pdf.cell(20, 8, "MENGE", border=1, fill=True, align="C")
        self.pdf.cell(30, 8, "EINZELPREIS", border=1, fill=True, align="R")
        self.pdf.cell(30, 8, "BETRAG", border=1, fill=True, align="R", ln=True)

        self.pdf.set_text_color(0, 0, 0)
        self.pdf.set_font("DejaVu", "", 9)

        for i, product in enumerate(invoice_data.get('produkte', [])):
            fill_color = (255, 255, 255) if i % 2 == 0 else (245, 245, 245)
            self.pdf.set_fill_color(*fill_color)

            total = product.get("qty", 0) * product.get("price", 0)
            y_before = self.pdf.get_y()

            self.pdf.multi_cell(90, 6, str(product.get("name")), border=1, fill=True, align="L")
            y_after = self.pdf.get_y()
            row_height = y_after - y_before

            self.pdf.set_xy(100, y_before)
            self.pdf.cell(20, row_height, str(product.get("qty", "")), border=1, fill=True, align="C")
            self.pdf.cell(30, row_height, f"€{float(product.get('price', 0)):.2f}", border=1, fill=True, align="R")
            self.pdf.cell(30, row_height, f"€{float(total):.2f}", border=1, fill=True, align="R", ln=True)

        self.pdf.ln(10)
