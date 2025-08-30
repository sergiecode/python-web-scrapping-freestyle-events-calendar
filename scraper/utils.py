"""
Utilidades comunes para todos los scrapers
Desarrollado por Sergie Code
"""

import sqlite3
import pandas as pd
import csv
import os
from datetime import datetime
from typing import List, Dict, Any
import time
import random

class EventDatabase:
    """Maneja la base de datos SQLite de eventos"""
    
    def __init__(self, db_path: str = "data/eventos.db"):
        self.db_path = db_path
        self.create_table()
    
    def create_table(self):
        """Crea la tabla de eventos si no existe"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS eventos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                fecha TEXT NOT NULL,
                hora TEXT,
                ciudad TEXT,
                pais TEXT,
                venue TEXT,
                organizador TEXT NOT NULL,
                link_oficial TEXT,
                descripcion TEXT,
                fecha_scraping TEXT NOT NULL,
                UNIQUE(nombre, fecha, organizador)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def insert_events(self, events: List[Dict[str, Any]]):
        """Inserta eventos en la base de datos"""
        if not events:
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for event in events:
            try:
                cursor.execute('''
                    INSERT OR REPLACE INTO eventos 
                    (nombre, fecha, hora, ciudad, pais, venue, organizador, link_oficial, descripcion, fecha_scraping)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    event.get('nombre', ''),
                    event.get('fecha', ''),
                    event.get('hora', ''),
                    event.get('ciudad', ''),
                    event.get('pais', ''),
                    event.get('venue', ''),
                    event.get('organizador', ''),
                    event.get('link_oficial', ''),
                    event.get('descripcion', ''),
                    datetime.now().isoformat()
                ))
            except sqlite3.Error as e:
                print(f"Error insertando evento {event.get('nombre', 'Unknown')}: {e}")
        
        conn.commit()
        conn.close()
    
    def get_all_events(self) -> List[Dict[str, Any]]:
        """Obtiene todos los eventos de la base de datos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM eventos ORDER BY fecha')
        rows = cursor.fetchall()
        
        columns = [description[0] for description in cursor.description]
        events = [dict(zip(columns, row)) for row in rows]
        
        conn.close()
        return events

class CSVExporter:
    """Maneja la exportación a CSV"""
    
    @staticmethod
    def export_events(events: List[Dict[str, Any]], csv_path: str = "data/eventos.csv"):
        """Exporta eventos a CSV"""
        if not events:
            return
        
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        
        df = pd.DataFrame(events)
        df.to_csv(csv_path, index=False, encoding='utf-8')
        print(f"✅ Exportados {len(events)} eventos a {csv_path}")

class ScrapingUtils:
    """Utilidades generales para scraping"""
    
    @staticmethod
    def random_delay(min_seconds: float = 1.0, max_seconds: float = 3.0):
        """Delay aleatorio entre requests"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Limpia texto extraído"""
        if not text:
            return ""
        return text.strip().replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    
    @staticmethod
    def parse_date(date_string: str) -> str:
        """Intenta parsear fecha en diferentes formatos"""
        if not date_string:
            return ""
        
        # Lista de formatos comunes
        formats = [
            "%d/%m/%Y",
            "%d-%m-%Y", 
            "%Y-%m-%d",
            "%d de %B de %Y",
            "%d %B %Y",
        ]
        
        # Mapeo de meses en español
        months_es = {
            'enero': 'January', 'febrero': 'February', 'marzo': 'March',
            'abril': 'April', 'mayo': 'May', 'junio': 'June',
            'julio': 'July', 'agosto': 'August', 'septiembre': 'September',
            'octubre': 'October', 'noviembre': 'November', 'diciembre': 'December'
        }
        
        # Reemplazar meses en español
        date_clean = date_string.lower()
        for es, en in months_es.items():
            date_clean = date_clean.replace(es, en)
        
        for fmt in formats:
            try:
                dt = datetime.strptime(date_clean, fmt.lower())
                return dt.strftime("%Y-%m-%d")
            except ValueError:
                continue
        
        return date_string
    
    @staticmethod
    def get_headers() -> Dict[str, str]:
        """Headers comunes para requests"""
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }

def log_scraping_result(scraper_name: str, events_count: int, success: bool = True):
    """Log del resultado del scraping"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "✅" if success else "❌"
    print(f"{status} [{timestamp}] {scraper_name}: {events_count} eventos encontrados")

def validate_event(event: Dict[str, Any]) -> bool:
    """Valida que un evento tenga los campos mínimos requeridos"""
    required_fields = ['nombre', 'fecha', 'organizador']
    return all(event.get(field) for field in required_fields)
