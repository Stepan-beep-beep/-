import sqlite3
from typing import List, Tuple, Optional
from config import DATABASE_NAME, LOW_STOCK_THRESHOLD


class Database:
    
    def __init__(self):
        self.conn: sqlite3.Connection = sqlite3.connect(DATABASE_NAME)
        self.cursor: sqlite3.Cursor = self.conn.cursor()
        self.create_table()
    
    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS materials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                quantity INTEGER DEFAULT 0,
                unit TEXT DEFAULT 'шт.',
                note TEXT DEFAULT ''
            )
        ''')
        self.conn.commit()
    
    def add_material(self, name: str, quantity: int, unit: str, note: str) -> bool:        
        try:
            self.cursor.execute(
                'INSERT INTO materials (name, quantity, unit, note) VALUES (?, ?, ?, ?)',
                (name, quantity, unit, note)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            raise
    
    def update_material(self, old_name: str, name: str, quantity: int, unit: str, note: str) -> bool:        
        try:
            self.cursor.execute(
                'UPDATE materials SET name=?, quantity=?, unit=?, note=? WHERE name=?',
                (name, quantity, unit, note, old_name)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            raise
    
    def delete_material(self, name: str) -> bool:        
        self.cursor.execute('DELETE FROM materials WHERE name=?', (name,))
        self.conn.commit()
        return True
    
    def update_quantity(self, name: str, quantity_change: int) -> int:        
        self.cursor.execute('SELECT quantity FROM materials WHERE name=?', (name,))
        result = self.cursor.fetchone()
        current = result[0] if result else 0
        
        new_quantity = current + quantity_change
        
        self.cursor.execute(
            'UPDATE materials SET quantity=? WHERE name=?',
            (new_quantity, name)
        )
        self.conn.commit()
        
        return new_quantity
    
    def get_current_quantity(self, name: str) -> int:
        self.cursor.execute('SELECT quantity FROM materials WHERE name=?', (name,))
        result = self.cursor.fetchone()
        return result[0] if result else 0
    
    def get_all_materials(self) -> List[Tuple]:        
        self.cursor.execute(
            'SELECT name, quantity, unit, note FROM materials ORDER BY name'
        )
        return self.cursor.fetchall()
    
    def search_materials(self, search_term: str) -> List[Tuple]:
        self.cursor.execute(
            '''SELECT name, quantity, unit, note FROM materials 
               WHERE name LIKE ? OR note LIKE ? 
               ORDER BY name''',
            (f'%{search_term}%', f'%{search_term}%')
        )
        return self.cursor.fetchall()
    
    def get_statistics(self) -> Tuple[Optional[int], Optional[int]]:
        self.cursor.execute('SELECT COUNT(*), SUM(quantity) FROM materials')
        return self.cursor.fetchone()
    
    def check_low_stock(self, name: str, quantity: int) -> bool:
        return quantity < LOW_STOCK_THRESHOLD
    
    def close(self):
        if self.conn:
            self.conn.close()
    
    def __del__(self):
        self.close()