from io import BytesIO
from invoice_generator.PDFBase import PDFBase
from invoice_generator.InvoiceHeader import InvoiceHeader
from invoice_generator.InvoiceClientSection import InvoiceClientSection
from invoice_generator.InvoiceProductTable import InvoiceProductTable
from invoice_generator.InvoiceFooter import InvoiceFooter

class InvoicePDF:
    def __init__(self):
        self.base = PDFBase()

    def generate(self, invoice_data: dict) -> BytesIO:
        InvoiceHeader(self.base.pdf).add(invoice_data)
        InvoiceClientSection(self.base.pdf).add(invoice_data)
        InvoiceProductTable(self.base.pdf).add(invoice_data)
        InvoiceFooter(self.base.pdf).add(invoice_data)

        pdf_buffer = BytesIO()
        self.base.pdf.output(pdf_buffer)
        return pdf_buffer
