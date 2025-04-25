class InvoiceClientSection:
    def __init__(self, pdf):
        self.pdf = pdf

    def add(self, invoice_data):
        box_height = 40
        box_top = self.pdf.get_y()

        self.pdf.set_fill_color(249, 249, 249)
        self.pdf.rect(10, box_top, 190, box_height, style='F')

        x = 17
        y = box_top + 6

        self.pdf.set_xy(x, y)
        self.pdf.set_font("DejaVu", "B", 10)
        self.pdf.set_text_color(33, 47, 61)
        self.pdf.cell(0, 6, "RECHNUNGSEMPFÄNGER", ln=True)

        self.pdf.set_xy(x, self.pdf.get_y() + 2)
        self.pdf.set_font("DejaVu", "B", 10)
        self.pdf.set_text_color(52, 58, 64)
        self.pdf.cell(0, 6, invoice_data.get('kunde_name'), ln=True)

        self.pdf.set_font("DejaVu", "", 9)
        self.pdf.set_text_color(73, 80, 87)

        address = f"{invoice_data.get('straße')}\n{invoice_data.get('plz')} {invoice_data.get('stadt')}"
        if invoice_data.get('land'):
            address += f", {invoice_data.get('land')}"
        self.pdf.set_xy(x, self.pdf.get_y() + 1.5)
        self.pdf.multi_cell(0, 5, address)
        self.pdf.set_xy(x, self.pdf.get_y() + 1.5)
        self.pdf.cell(0, 5, f"E-Mail: {invoice_data.get('email')}", ln=True)

        self.pdf.set_y(box_top + box_height + 5)
