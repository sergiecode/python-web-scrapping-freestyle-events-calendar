"""
Script principal para ejecutar todos los scrapers
Desarrollado por Sergie Code
"""

import sys
import os
from datetime import datetime

# Agregar el directorio padre al path para imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scraper.redbull import RedBullScraper
from scraper.fms import FMSScraper
from scraper.godlevel import GodLevelScraper
from scraper.supremacia import SupremaciaScraper
from scraper.tickets import TicketsScraper
from scraper.utils import EventDatabase, CSVExporter, log_scraping_result

def run_all_scrapers():
    """Ejecuta todos los scrapers y guarda los datos"""
    print("🚀 Iniciando scraping de eventos de freestyle...")
    print(f"📅 Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    all_events = []
    
    # Instanciar base de datos
    db = EventDatabase()
    
    # Scrapers a ejecutar
    scrapers = [
        ("Red Bull Batalla", RedBullScraper()),
        ("Urban Roosters (FMS)", FMSScraper()),
        ("God Level", GodLevelScraper()),
        ("Supremacía MC", SupremaciaScraper()),
        ("Sitios de Tickets", TicketsScraper())
    ]
    
    # Ejecutar cada scraper
    for name, scraper in scrapers:
        try:
            print(f"\n🔄 Ejecutando scraper: {name}")
            events = scraper.scrape_events()
            
            if events:
                all_events.extend(events)
                # Guardar en base de datos inmediatamente
                db.insert_events(events)
                print(f"✅ {name}: {len(events)} eventos procesados")
            else:
                print(f"⚠️ {name}: No se encontraron eventos")
                
        except Exception as e:
            print(f"❌ Error en scraper {name}: {e}")
            log_scraping_result(name, 0, False)
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN FINAL")
    print("=" * 60)
    
    if all_events:
        # Exportar a CSV
        CSVExporter.export_events(all_events)
        
        # Estadísticas por organizador
        organizers = {}
        countries = {}
        
        for event in all_events:
            org = event.get('organizador', 'Unknown')
            country = event.get('pais', 'Unknown')
            
            organizers[org] = organizers.get(org, 0) + 1
            countries[country] = countries.get(country, 0) + 1
        
        print(f"📈 Total de eventos encontrados: {len(all_events)}")
        print(f"🗃️ Eventos guardados en: data/eventos.db")
        print(f"📄 Eventos exportados a: data/eventos.csv")
        
        print("\n📊 Por organizador:")
        for org, count in sorted(organizers.items(), key=lambda x: x[1], reverse=True):
            print(f"   • {org}: {count} eventos")
        
        print("\n🌍 Por país:")
        for country, count in sorted(countries.items(), key=lambda x: x[1], reverse=True):
            print(f"   • {country}: {count} eventos")
        
        # Próximos eventos (ordenados por fecha)
        print("\n📅 Próximos eventos:")
        sorted_events = sorted([e for e in all_events if e.get('fecha')], 
                             key=lambda x: x['fecha'])
        
        for event in sorted_events[:5]:  # Mostrar solo los próximos 5
            fecha = event.get('fecha', 'N/A')
            nombre = event.get('nombre', 'N/A')
            pais = event.get('pais', 'N/A')
            print(f"   • {fecha} - {nombre} ({pais})")
        
    else:
        print("⚠️ No se encontraron eventos en ninguna fuente")
        print("💡 Verifica la conexión a internet y los sitios web")
    
    print("\n✨ Scraping completado!")
    print("🌐 Puedes iniciar la aplicación web con: python webapp/app.py")

def show_database_stats():
    """Muestra estadísticas de la base de datos"""
    try:
        db = EventDatabase()
        events = db.get_all_events()
        
        print(f"📊 Estadísticas de la base de datos:")
        print(f"   Total de eventos: {len(events)}")
        
        if events:
            # Agrupar por organizador
            organizers = {}
            for event in events:
                org = event.get('organizador', 'Unknown')
                organizers[org] = organizers.get(org, 0) + 1
            
            print("\n   Por organizador:")
            for org, count in organizers.items():
                print(f"     • {org}: {count}")
    
    except Exception as e:
        print(f"❌ Error accediendo a la base de datos: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--stats":
        show_database_stats()
    else:
        run_all_scrapers()
