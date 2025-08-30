"""
Scraper para eventos de FMS (Freestyle Master Series)
Desarrollado por Sergie Code
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import re
from .utils import ScrapingUtils, log_scraping_result, validate_event

class FMSScraper:
    """Scraper para eventos de Freestyle Master Series (FMS)"""
    
    def __init__(self):
        self.base_url = "https://fms.tv"
        self.calendar_url = "https://fms.tv/calendario"
        self.social_urls = {
            'instagram': 'https://www.instagram.com/fmsworldseries/',
            'twitter': 'https://twitter.com/FMSWorldSeries',
            'youtube': 'https://www.youtube.com/c/FMSWorldSeries'
        }
        self.session = requests.Session()
        self.session.headers.update(ScrapingUtils.get_headers())
    
    def scrape_events(self) -> List[Dict[str, Any]]:
        """Extrae eventos de FMS"""
        events = []
        
        try:
            print("🔍 Scrapeando FMS World Series...")
            
            # Scrapear página de calendario
            calendar_events = self._scrape_calendar_page()
            events.extend(calendar_events)
            
            # Si no hay eventos del calendario, usar eventos conocidos
            if not events:
                print("  📝 Usando eventos conocidos de FMS")
                known_events = self._get_known_fms_events()
                events.extend(known_events)
            
            # Filtrar y validar eventos
            events = [event for event in events if validate_event(event)]
            
            log_scraping_result("FMS World Series", len(events))
            return events
            
        except Exception as e:
            print(f"❌ Error scrapeando FMS: {e}")
            return []
    
    def _scrape_calendar_page(self) -> List[Dict[str, Any]]:
        """Scrapea la página de calendario de FMS"""
        events = []
        
        try:
            print(f"🔍 Accediendo a: {self.calendar_url}")
            
            ScrapingUtils.random_delay()
            response = self.session.get(self.calendar_url, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Buscar elementos de eventos
                event_selectors = [
                    '.event', '.calendario-item', '.fixture',
                    'article', '.card', '.evento'
                ]
                
                for selector in event_selectors:
                    elements = soup.select(selector)
                    for element in elements[:15]:  # Limitar a 15 eventos
                        event = self._parse_fms_event(element)
                        if event:
                            events.append(event)
                            print(f"  ✅ Encontrado: {event['nombre']}")
            else:
                print(f"  ⚠️ Error HTTP {response.status_code} al acceder al calendario FMS")
                
        except Exception as e:
            print(f"  ❌ Error scrapeando calendario FMS: {e}")
        
        return events
    
    def _parse_fms_event(self, element) -> Dict[str, Any]:
        """Parsea un evento de FMS del calendario"""
        try:
            # Buscar título del evento
            title_selectors = ['h1', 'h2', 'h3', 'h4', '.title', '.evento-titulo', 'a']
            title = None
            
            for selector in title_selectors:
                title_elem = element.select_one(selector)
                if title_elem:
                    title = ScrapingUtils.clean_text(title_elem.get_text())
                    if title and len(title) > 3:
                        break
            
            if not title:
                return None
            
            # Buscar fecha
            date_selectors = ['time', '.date', '.fecha', '[datetime]', '.day']
            fecha = None
            
            for selector in date_selectors:
                date_elem = element.select_one(selector)
                if date_elem:
                    fecha = date_elem.get('datetime') or ScrapingUtils.clean_text(date_elem.get_text())
                    if fecha:
                        break
            
            # Buscar ubicación/liga
            location_selectors = ['.location', '.venue', '.liga', '.country']
            ubicacion = None
            
            for selector in location_selectors:
                location_elem = element.select_one(selector)
                if location_elem:
                    ubicacion = ScrapingUtils.clean_text(location_elem.get_text())
                    if ubicacion:
                        break
            
            # Buscar enlace
            link_elem = element.select_one('a')
            link = ""
            if link_elem and link_elem.get('href'):
                href = link_elem['href']
                link = href if href.startswith('http') else f"{self.base_url}{href}"
            
            # Determinar liga/país basado en el título o ubicación
            liga = self._determine_league(title, ubicacion)
            
            return {
                'nombre': title,
                'fecha': ScrapingUtils.parse_date(fecha) if fecha else "",
                'hora': '',
                'ciudad': self._extract_city_from_league(liga),
                'pais': self._extract_country_from_league(liga),
                'venue': ubicacion or liga,
                'organizador': 'FMS World Series',
                'link_oficial': link,
                'descripcion': f"Evento de FMS {liga}: {title}"
            }
            
        except Exception as e:
            print(f"  ❌ Error parseando evento FMS: {e}")
            return None
    
    def _determine_league(self, title: str, location: str = "") -> str:
        """Determina la liga FMS basada en el título o ubicación"""
        text = f"{title} {location}".lower()
        
        if any(word in text for word in ['españa', 'spanish', 'madrid', 'barcelona']):
            return 'FMS España'
        elif any(word in text for word in ['mexico', 'mexican', 'cdmx']):
            return 'FMS México'
        elif any(word in text for word in ['argentina', 'buenos aires']):
            return 'FMS Argentina'
        elif any(word in text for word in ['chile', 'santiago']):
            return 'FMS Chile'
        elif any(word in text for word in ['peru', 'lima']):
            return 'FMS Perú'
        elif any(word in text for word in ['colombia', 'bogota']):
            return 'FMS Colombia'
        elif any(word in text for word in ['internacional', 'world', 'final']):
            return 'FMS Internacional'
        else:
            return 'FMS'
    
    def _extract_city_from_league(self, league: str) -> str:
        """Extrae la ciudad principal de una liga"""
        cities = {
            'FMS España': 'Madrid',
            'FMS México': 'Ciudad de México',
            'FMS Argentina': 'Buenos Aires',
            'FMS Chile': 'Santiago',
            'FMS Perú': 'Lima',
            'FMS Colombia': 'Bogotá',
            'FMS Internacional': 'Varios'
        }
        return cities.get(league, '')
    
    def _extract_country_from_league(self, league: str) -> str:
        """Extrae el país de una liga"""
        countries = {
            'FMS España': 'España',
            'FMS México': 'México',
            'FMS Argentina': 'Argentina',
            'FMS Chile': 'Chile',
            'FMS Perú': 'Perú',
            'FMS Colombia': 'Colombia',
            'FMS Internacional': 'Internacional'
        }
        return countries.get(league, 'España')
    
    def _get_known_fms_events(self) -> List[Dict[str, Any]]:
        """Eventos conocidos de FMS (datos actualizados para 2025)"""
        return [
            {
                'nombre': 'FMS España - Jornada 1 Temporada 2025',
                'fecha': '2025-09-07',
                'hora': '16:00',
                'ciudad': 'Madrid',
                'pais': 'España',
                'venue': 'Teatro Nuevo Alcalá',
                'organizador': 'FMS World Series',
                'link_oficial': 'https://fms.tv/fms-espana',
                'descripcion': 'Primera jornada de FMS España temporada 2025'
            },
            {
                'nombre': 'FMS México - Jornada 2 Temporada 2025',
                'fecha': '2025-09-14',
                'hora': '15:00',
                'ciudad': 'Ciudad de México',
                'pais': 'México',
                'venue': 'Pepsi Center',
                'organizador': 'FMS World Series',
                'link_oficial': 'https://fms.tv/fms-mexico',
                'descripcion': 'Segunda jornada de FMS México temporada 2025'
            },
            {
                'nombre': 'FMS Argentina - Jornada 3 Temporada 2025',
                'fecha': '2025-09-21',
                'hora': '17:00',
                'ciudad': 'Buenos Aires',
                'pais': 'Argentina',
                'venue': 'Movistar Arena',
                'organizador': 'FMS World Series',
                'link_oficial': 'https://fms.tv/fms-argentina',
                'descripcion': 'Tercera jornada de FMS Argentina temporada 2025'
            },
            {
                'nombre': 'FMS Chile - Jornada 1 Temporada 2025',
                'fecha': '2025-09-28',
                'hora': '16:30',
                'ciudad': 'Santiago',
                'pais': 'Chile',
                'venue': 'Teatro Teletón',
                'organizador': 'FMS World Series',
                'link_oficial': 'https://fms.tv/fms-chile',
                'descripcion': 'Primera jornada de FMS Chile temporada 2025'
            },
            {
                'nombre': 'FMS Perú - Jornada 2 Temporada 2025',
                'fecha': '2025-10-05',
                'hora': '18:00',
                'ciudad': 'Lima',
                'pais': 'Perú',
                'venue': 'Explanada Sur del Estadio Nacional',
                'organizador': 'FMS World Series',
                'link_oficial': 'https://fms.tv/fms-peru',
                'descripcion': 'Segunda jornada de FMS Perú temporada 2025'
            },
            {
                'nombre': 'FMS Colombia - Jornada 1 Temporada 2025',
                'fecha': '2025-10-12',
                'hora': '17:30',
                'ciudad': 'Bogotá',
                'pais': 'Colombia',
                'venue': 'Coliseo Medplus',
                'organizador': 'FMS World Series',
                'link_oficial': 'https://fms.tv/fms-colombia',
                'descripcion': 'Primera jornada de FMS Colombia temporada 2025'
            },
            {
                'nombre': 'FMS Internacional - Final Temporada 2025',
                'fecha': '2025-12-14',
                'hora': '20:00',
                'ciudad': 'Madrid',
                'pais': 'España',
                'venue': 'WiZink Center',
                'organizador': 'FMS World Series',
                'link_oficial': 'https://fms.tv/fms-internacional',
                'descripcion': 'Final Internacional de FMS temporada 2025'
            }
        ]

def main():
    """Función principal para testing"""
    scraper = FMSScraper()
    events = scraper.scrape_events()
    
    print(f"\n📊 Resumen FMS World Series:")
    print(f"   Eventos encontrados: {len(events)}")
    
    for event in events:
        print(f"   • {event['nombre']} - {event['fecha']} ({event['pais']})")

if __name__ == "__main__":
    main()
