import qrcode
import tempfile
import os

class ProductQRGenerator:
    @staticmethod
    def generate_qr(link: str) -> str:
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=4,
                border=2,
            )
            qr.add_data(link)
            qr.make(fit=True)

            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as f:
                img = qr.make_image(fill_color="black", back_color="white")
                img.save(f.name)
                return f.name
        except Exception as e:
            print(f"Failed to generate QR: {e}")
            return ""
