import sqlite3
from pathlib import Path
from config import DATABASE_FILE
from typing import List, Dict, Optional, Tuple
import pandas as pd

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_FILE)
        self._init_tables()
        
    def _init_tables(self):
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS invoices (
                invoice_no INTEGER PRIMARY KEY,
                client TEXT,
                email TEXT,
                date TEXT,
                delivery TEXT,
                total REAL,
                filename TEXT
            )''')
            self.conn.execute('''CREATE TABLE IF NOT EXISTS clients (
                name TEXT PRIMARY KEY,
                email TEXT,
                street TEXT,
                plz TEXT,
                city TEXT,
                country TEXT
            )''')
    
    def get_client_names(self) -> List[str]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM clients ORDER BY name")
        return [row[0] for row in cursor.fetchall()]
    
    def get_client(self, name: str) -> Optional[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM clients WHERE name = ?", (name,))
        row = cursor.fetchone()
        if row:
            return {
                "name": row[0],
                "email": row[1],
                "street": row[2],
                "plz": row[3],
                "city": row[4],
                "country": row[5]
            }
        return None
    
    def save_client(self, client_data: Dict) -> None:
        with self.conn:
            self.conn.execute(
                "REPLACE INTO clients VALUES (?, ?, ?, ?, ?, ?)",
                (
                    client_data["name"],
                    client_data["email"],
                    client_data["street"],
                    client_data["plz"],
                    client_data["city"],
                    client_data["country"]
                )
            )
    
    def save_invoice(self, invoice_data: Dict) -> None:
        with self.conn:
            self.conn.execute(
                "INSERT INTO invoices VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    invoice_data["invoice_no"],
                    invoice_data["client"],
                    invoice_data["email"],
                    invoice_data["date"],
                    invoice_data["delivery"],
                    invoice_data["total"],
                    invoice_data["filename"]
                )
            )
    
    def get_invoices(self, search_name: str = None, search_date: str = None) -> pd.DataFrame:
        query = "SELECT * FROM invoices"
        params = []
        
        if search_name or search_date:
            conditions = []
            if search_name:
                conditions.append("client LIKE ?")
                params.append(f"%{search_name}%")
            if search_date:
                conditions.append("date LIKE ?")
                params.append(f"%{search_date}%")
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY invoice_no DESC"
        
        # Ensure params is always a list
        return pd.read_sql_query(query, self.conn, params=params)
    
    def close(self):
        self.conn.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()