#!/usr/bin/env python3
"""
Script to add sample events to the database if it's empty
"""

from scraper.utils import EventDatabase
import os

def add_sample_events():
    """Add sample events to the database if it's empty"""
    db_path = 'data/eventos.db'
    
    if not os.path.exists(db_path):
        print("Database not found, creating...")
        os.makedirs('data', exist_ok=True)
    
    db = EventDatabase(db_path)
    events = db.get_all_events()
    print(f'Found {len(events)} events in database')
    
    if len(events) == 0:
        print('Adding sample events...')
        sample_events = [
            {
                'titulo': 'Red Bull Batalla España 2025',
                'fecha': '2025-12-15',
                'hora': '20:00',
                'lugar': 'Palacio de Deportes',
                'ciudad': 'Madrid',
                'pais': 'España',
                'organizador': 'Red Bull',
                'descripcion': 'Final nacional de Red Bull Batalla',
                'precio': 'Gratis',
                'link': 'https://redbull.com/batalla'
            },
            {
                'titulo': 'FMS España Jornada 8',
                'fecha': '2025-11-20',
                'hora': '19:00',
                'lugar': 'WiZink Center',
                'ciudad': 'Madrid',
                'pais': 'España',
                'organizador': 'Urban Roosters',
                'descripcion': 'Jornada 8 de la Freestyle Master Series',
                'precio': '25€ - 50€',
                'link': 'https://fms.com'
            },
            {
                'titulo': 'God Level Argentina',
                'fecha': '2025-10-30',
                'hora': '21:00',
                'lugar': 'Luna Park',
                'ciudad': 'Buenos Aires',
                'pais': 'Argentina',
                'organizador': 'God Level',
                'descripcion': 'Evento especial de God Level en Argentina',
                'precio': '30€',
                'link': 'https://godlevel.com'
            },
            {
                'titulo': 'Supremacía MC Venezuela',
                'fecha': '2025-11-05',
                'hora': '20:30',
                'lugar': 'Teatro Principal',
                'ciudad': 'Caracas',
                'pais': 'Venezuela',
                'organizador': 'Supremacía',
                'descripcion': 'Batalla de freestyle en Venezuela',
                'precio': '15€',
                'link': 'https://supremacia.com'
            },
            {
                'titulo': 'FMS México Jornada 6',
                'fecha': '2025-09-25',
                'hora': '19:30',
                'lugar': 'Arena Ciudad de México',
                'ciudad': 'Ciudad de México',
                'pais': 'México',
                'organizador': 'Urban Roosters',
                'descripcion': 'Jornada 6 de FMS México',
                'precio': '20€ - 40€',
                'link': 'https://fms.com/mexico'
            }
        ]
        
        db.insert_events(sample_events)
        print(f'✅ Added {len(sample_events)} sample events to the database')
        
        # Verify events were added
        events = db.get_all_events()
        print(f'✅ Database now has {len(events)} events')
        
        print("\nSample events added:")
        for event in sample_events:
            print(f"  • {event['titulo']} - {event['fecha']} ({event['pais']})")
            
    else:
        print('✅ Database already has events, no need to add sample data')
        print(f"Events found:")
        for event in events[:5]:  # Show first 5 events
            titulo = event.get('titulo') or event.get('nombre', 'Sin título')
            fecha = event.get('fecha', 'Sin fecha')
            pais = event.get('pais', 'Sin país')
            print(f"  • {titulo} - {fecha} ({pais})")

if __name__ == "__main__":
    add_sample_events()
