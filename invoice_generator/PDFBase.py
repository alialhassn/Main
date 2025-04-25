from fpdf import FPDF2
from config import FONT_REGULAR, FONT_BOLD, FONT_ITALIC

class PDFBase:
    def __init__(self):
        self.pdf = FPDF()
        self.page_width = 210  # A4
        self.margin = 10

        self._setup_fonts()
        self.pdf.set_auto_page_break(auto=True, margin=15)
        self.pdf.add_page()

    def _setup_fonts(self):
        try:
            self.pdf.add_font("DejaVu", "", str(FONT_REGULAR), uni=True)
            self.pdf.add_font("DejaVu", "B", str(FONT_BOLD), uni=True)
            self.pdf.add_font("DejaVu", "I", str(FONT_ITALIC), uni=True)
            self.pdf.set_font("DejaVu", "", 10)
        except RuntimeError:
            self.pdf.set_font("Arial", "", 10)
