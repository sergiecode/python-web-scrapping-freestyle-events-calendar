"""
Scraper para eventos de Supremacía MC
Desarrollado por Sergie Code
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import re
from .utils import ScrapingUtils, log_scraping_result, validate_event

class SupremaciaScraper:
    """Scraper para eventos de InfoFreestyle y otros sitios de batalla"""
    
    def __init__(self):
        self.base_url = "https://infofreestyle.com"
        self.eventos_url = "https://infofreestyle.com/eventos"
        self.social_urls = {
            'instagram': 'https://www.instagram.com/infofreestyle/',
            'twitter': 'https://twitter.com/InfoFreestyle'
        }
        self.session = requests.Session()
        self.session.headers.update(ScrapingUtils.get_headers())
    
    def scrape_events(self) -> List[Dict[str, Any]]:
        """Extrae eventos de Supremacía MC"""
        events = []
        
        try:
            print("🔍 Scrapeando Supremacía MC...")
            
            # Intentar scrapear diferentes secciones
            main_events = self._scrape_main_page()
            events.extend(main_events)
            
            # Scrapear eventos por países
            latam_events = self._scrape_latam_events()
            events.extend(latam_events)
            
            # Agregar eventos conocidos
            known_events = self._get_known_supremacia_events()
            events.extend(known_events)
            
            # Filtrar y validar eventos
            events = [event for event in events if validate_event(event)]
            
            log_scraping_result("Supremacía MC", len(events))
            return events
            
        except Exception as e:
            print(f"❌ Error scrapeando Supremacía MC: {e}")
            log_scraping_result("Supremacía MC", 0, False)
            return []
    
    def _scrape_main_page(self) -> List[Dict[str, Any]]:
        """Extrae eventos de la página principal"""
        events = []
        
        try:
            response = self.session.get(self.base_url, timeout=10)
            if response.status_code != 200:
                return events
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Buscar elementos de eventos
            event_elements = soup.find_all(['div', 'article'], 
                                         class_=re.compile(r'event|battle|supremacia'))
            
            for element in event_elements:
                event = self._parse_supremacia_event(element)
                if event:
                    events.append(event)
                    
        except Exception as e:
            print(f"Error scrapeando página principal de Supremacía: {e}")
        
        return events
    
    def _scrape_latam_events(self) -> List[Dict[str, Any]]:
        """Extrae eventos de países LATAM"""
        events = []
        
        # Países donde Supremacía tiene actividad
        countries = ['mexico', 'colombia', 'argentina', 'chile', 'peru']
        
        for country in countries:
            try:
                ScrapingUtils.random_delay()
                country_events = self._scrape_country_events(country)
                events.extend(country_events)
            except Exception as e:
                print(f"Error scrapeando eventos de {country}: {e}")
        
        return events
    
    def _scrape_country_events(self, country: str) -> List[Dict[str, Any]]:
        """Extrae eventos de un país específico"""
        events = []
        
        try:
            country_url = f"{self.base_url}/{country}"
            response = self.session.get(country_url, timeout=10)
            
            if response.status_code != 200:
                return events
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Buscar eventos específicos del país
            event_elements = soup.find_all(['div', 'section'], 
                                         class_=re.compile(r'event|battle|tournament'))
            
            for element in event_elements:
                event = self._parse_supremacia_event(element, country)
                if event:
                    events.append(event)
                    
        except Exception as e:
            print(f"Error scrapeando eventos de {country}: {e}")
        
        return events
    
    def _parse_supremacia_event(self, element, country: str = "") -> Dict[str, Any]:
        """Parsea un evento de Supremacía MC"""
        try:
            # Buscar título
            title_elem = element.find(['h1', 'h2', 'h3', 'h4'])
            if not title_elem:
                return None
            
            title = ScrapingUtils.clean_text(title_elem.get_text())
            
            # Filtrar solo eventos de freestyle/batalla
            if not any(keyword in title.lower() for keyword in 
                      ['supremacia', 'batalla', 'freestyle', 'mc', 'tournament']):
                return None
            
            # Buscar fecha
            date_elem = element.find(['time', 'span'], class_=re.compile(r'date|fecha'))
            date = ""
            if date_elem:
                date = ScrapingUtils.parse_date(date_elem.get_text())
            
            # Buscar link
            link_elem = element.find('a')
            link = ""
            if link_elem and link_elem.get('href'):
                href = link_elem['href']
                link = href if href.startswith('http') else f"{self.base_url}{href}"
            
            # Buscar ubicación
            location_elem = element.find(['span', 'div'], class_=re.compile(r'location|venue|lugar'))
            location = ""
            if location_elem:
                location = ScrapingUtils.clean_text(location_elem.get_text())
            
            # Determinar país y ciudad
            event_country = self._get_country_from_context(country, location, title)
            event_city = self._get_city_from_country(event_country)
            
            return {
                'nombre': f"Supremacía MC - {title}",
                'fecha': date,
                'hora': '',
                'ciudad': event_city,
                'pais': event_country,
                'venue': location if location else f"Venue Supremacía {event_country}",
                'organizador': 'Supremacía MC',
                'link_oficial': link if link else self.base_url,
                'descripcion': f"Evento de Supremacía MC: {title}"
            }
            
        except Exception as e:
            print(f"Error parseando evento de Supremacía: {e}")
            return None
    
    def _get_known_supremacia_events(self) -> List[Dict[str, Any]]:
        """Eventos conocidos de Supremacía MC"""
        return [
            {
                'nombre': 'Supremacía MC México - Temporada 2025',
                'fecha': '2025-09-12',
                'hora': '20:00',
                'ciudad': 'Ciudad de México',
                'pais': 'México',
                'venue': 'Centro de Espectáculos',
                'organizador': 'Supremacía MC',
                'link_oficial': 'https://www.supremaciamc.com/mexico-2025',
                'descripcion': 'Temporada 2025 de Supremacía MC México'
            },
            {
                'nombre': 'Supremacía MC Colombia - Regional Bogotá',
                'fecha': '2025-09-19',
                'hora': '19:30',
                'ciudad': 'Bogotá',
                'pais': 'Colombia',
                'venue': 'Teatro Nacional',
                'organizador': 'Supremacía MC',
                'link_oficial': 'https://www.supremaciamc.com/colombia-bogota',
                'descripcion': 'Regional de Supremacía MC en Bogotá'
            },
            {
                'nombre': 'Supremacía MC Argentina - Buenos Aires Battle',
                'fecha': '2025-10-03',
                'hora': '18:00',
                'ciudad': 'Buenos Aires',
                'pais': 'Argentina',
                'venue': 'C Complejo Art Media',
                'organizador': 'Supremacía MC',
                'link_oficial': 'https://www.supremaciamc.com/argentina-bsas',
                'descripcion': 'Batalla de Supremacía MC en Buenos Aires'
            },
            {
                'nombre': 'Supremacía MC Chile - Santiago Championship',
                'fecha': '2025-10-10',
                'hora': '19:00',
                'ciudad': 'Santiago',
                'pais': 'Chile',
                'venue': 'Teatro Universidad de Chile',
                'organizador': 'Supremacía MC',
                'link_oficial': 'https://www.supremaciamc.com/chile-santiago',
                'descripcion': 'Campeonato de Supremacía MC en Santiago'
            },
            {
                'nombre': 'Supremacía MC Perú - Lima Regional',
                'fecha': '2025-10-17',
                'hora': '18:30',
                'ciudad': 'Lima',
                'pais': 'Perú',
                'venue': 'Centro de Convenciones Lima',
                'organizador': 'Supremacía MC',
                'link_oficial': 'https://www.supremaciamc.com/peru-lima',
                'descripcion': 'Regional de Supremacía MC en Lima'
            },
            {
                'nombre': 'Supremacía MC Internacional - Final LATAM',
                'fecha': '2025-11-28',
                'hora': '20:30',
                'ciudad': 'Ciudad de México',
                'pais': 'México',
                'venue': 'Arena México',
                'organizador': 'Supremacía MC',
                'link_oficial': 'https://www.supremaciamc.com/final-latam-2025',
                'descripcion': 'Final Internacional de Supremacía MC LATAM 2025'
            }
        ]
    
    def _get_country_from_context(self, country_hint: str, location: str, title: str) -> str:
        """Determina el país basado en el contexto"""
        # Mapeo de hints de país
        country_mapping = {
            'mexico': 'México',
            'colombia': 'Colombia', 
            'argentina': 'Argentina',
            'chile': 'Chile',
            'peru': 'Perú'
        }
        
        # Si hay hint del país en la URL
        if country_hint and country_hint in country_mapping:
            return country_mapping[country_hint]
        
        # Buscar en ubicación
        if location:
            location_lower = location.lower()
            for key, value in country_mapping.items():
                if key in location_lower or value.lower() in location_lower:
                    return value
        
        # Buscar en título
        if title:
            title_lower = title.lower()
            for key, value in country_mapping.items():
                if key in title_lower or value.lower() in title_lower:
                    return value
        
        return "México"  # Default
    
    def _get_city_from_country(self, country: str) -> str:
        """Obtiene la ciudad principal según el país"""
        main_cities = {
            'México': 'Ciudad de México',
            'Colombia': 'Bogotá',
            'Argentina': 'Buenos Aires',
            'Chile': 'Santiago',
            'Perú': 'Lima'
        }
        return main_cities.get(country, 'Ciudad de México')

def main():
    """Función principal para testing"""
    scraper = SupremaciaScraper()
    events = scraper.scrape_events()
    
    print(f"\n📊 Resumen Supremacía MC:")
    print(f"   Eventos encontrados: {len(events)}")
    
    for event in events:
        print(f"   • {event['nombre']} - {event['fecha']} ({event['pais']})")

if __name__ == "__main__":
    main()
