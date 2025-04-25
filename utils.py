from pathlib import Path
from config import INVOICE_NUMBER_FILE
import os

def get_invoice_number() -> int:
    """Get and increment the invoice number"""
    if not INVOICE_NUMBER_FILE.exists():
        with open(INVOICE_NUMBER_FILE, "w") as f:
            f.write("1001")
    
    with open(INVOICE_NUMBER_FILE, "r") as f:
        num = int(f.read())
    
    with open(INVOICE_NUMBER_FILE, "w") as f:
        f.write(str(num + 1))
    
    return num

def validate_invoice_data(data: dict) -> bool:
    """Validate invoice data before processing"""
    required_fields = [
        'kunde_name', 'email', 'straße', 'plz', 
        'stadt', 'land', 'produkte'
    ]
    
    for field in required_fields:
        if not data.get(field):
            return False
    
    if not isinstance(data['produkte'], list) or len(data['produkte']) == 0:
        return False
    
    for product in data['produkte']:
        if not all(key in product for key in ['name', 'qty', 'price']):
            return False
    
    return True