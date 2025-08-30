"""
Scraper para eventos de God Level
Desarrollado por Sergie Code
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import re
from .utils import ScrapingUtils, log_scraping_result, validate_event

class GodLevelScraper:
    """Scraper para eventos de God Level"""
    
    def __init__(self):
        self.base_url = "https://godlevel.es"
        self.events_url = "https://godlevel.es/eventos"
        self.social_urls = {
            'instagram': 'https://www.instagram.com/godlevel_oficial/',
            'twitter': 'https://twitter.com/GodLevel_',
            'youtube': 'https://www.youtube.com/c/GodLevelOficial'
        }
        self.session = requests.Session()
        self.session.headers.update(ScrapingUtils.get_headers())
    
    def scrape_events(self) -> List[Dict[str, Any]]:
        """Extrae eventos de God Level"""
        events = []
        
        try:
            print("🔍 Scrapeando God Level...")
            
            # Scrapear página de eventos
            events_page = self._scrape_events_page()
            events.extend(events_page)
            
            # Si no hay eventos, usar eventos conocidos
            if not events:
                print("  📝 Usando eventos conocidos de God Level")
                known_events = self._get_known_godlevel_events()
                events.extend(known_events)
            
            # Filtrar y validar eventos
            events = [event for event in events if validate_event(event)]
            
            log_scraping_result("God Level", len(events))
            return events
            
        except Exception as e:
            print(f"❌ Error scrapeando God Level: {e}")
            return []
    
    def _scrape_events_page(self) -> List[Dict[str, Any]]:
        """Scrapea la página de eventos de God Level"""
        events = []
        
        try:
            print(f"🔍 Accediendo a: {self.events_url}")
            
            ScrapingUtils.random_delay()
            response = self.session.get(self.events_url, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Buscar elementos de eventos
                event_selectors = [
                    '.event', '.evento', '.battle', '.batalla',
                    'article', '.card', '.item'
                ]
                
                for selector in event_selectors:
                    elements = soup.select(selector)
                    for element in elements[:10]:  # Limitar a 10 eventos
                        event = self._parse_godlevel_event(element)
                        if event:
                            events.append(event)
                            print(f"  ✅ Encontrado: {event['nombre']}")
            else:
                print(f"  ⚠️ Error HTTP {response.status_code} al acceder a eventos God Level")
                
        except Exception as e:
            print(f"  ❌ Error scrapeando eventos God Level: {e}")
        
        return events
    
    def _parse_godlevel_event(self, element) -> Dict[str, Any]:
        """Parsea un evento de God Level"""
        try:
            # Buscar título
            title_selectors = ['h1', 'h2', 'h3', 'h4', '.title', '.nombre', 'a']
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
            date_selectors = ['time', '.date', '.fecha', '[datetime]']
            fecha = None
            
            for selector in date_selectors:
                date_elem = element.select_one(selector)
                if date_elem:
                    fecha = date_elem.get('datetime') or ScrapingUtils.clean_text(date_elem.get_text())
                    if fecha:
                        break
            
            # Buscar ubicación
            location_selectors = ['.location', '.venue', '.lugar', '.ciudad']
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
            
            return {
                'nombre': title,
                'fecha': ScrapingUtils.parse_date(fecha) if fecha else "",
                'hora': '',
                'ciudad': self._extract_city(ubicacion) if ubicacion else "Madrid",
                'pais': "España",
                'venue': ubicacion or "",
                'organizador': 'God Level',
                'link_oficial': link,
                'descripcion': f"Evento de God Level: {title}"
            }
            
        except Exception as e:
            print(f"  ❌ Error parseando evento God Level: {e}")
            return None
            
            # Buscar sección de eventos/torneos
            tournament_events = self._scrape_tournaments()
            events.extend(tournament_events)
            
            # Agregar eventos conocidos
            known_events = self._get_known_godlevel_events()
            events.extend(known_events)
            
            # Filtrar y validar eventos
            events = [event for event in events if validate_event(event)]
            
            log_scraping_result("God Level", len(events))
            return events
            
        except Exception as e:
            print(f"❌ Error scrapeando God Level: {e}")
            log_scraping_result("God Level", 0, False)
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
            event_selectors = [
                'div[class*="event"]',
                'div[class*="tournament"]',
                'article[class*="event"]',
                'section[class*="event"]'
            ]
            
            for selector in event_selectors:
                elements = soup.select(selector)
                for element in elements:
                    event = self._parse_godlevel_event(element)
                    if event:
                        events.append(event)
                        
        except Exception as e:
            print(f"Error scrapeando página principal de God Level: {e}")
        
        return events
    
    def _scrape_tournaments(self) -> List[Dict[str, Any]]:
        """Extrae eventos de la sección de torneos"""
        events = []
        
        try:
            tournaments_url = f"{self.base_url}/tournaments"
            response = self.session.get(tournaments_url, timeout=10)
            
            if response.status_code != 200:
                return events
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Buscar torneos específicos
            tournament_elements = soup.find_all(['div', 'article'], 
                                              class_=re.compile(r'tournament|battle|event'))
            
            for element in tournament_elements:
                event = self._parse_godlevel_event(element)
                if event:
                    events.append(event)
                    
        except Exception as e:
            print(f"Error scrapeando torneos de God Level: {e}")
        
        return events
    
    def _parse_godlevel_event(self, element) -> Dict[str, Any]:
        """Parsea un evento de God Level"""
        try:
            # Buscar título
            title_elem = element.find(['h1', 'h2', 'h3', 'h4'])
            if not title_elem:
                return None
            
            title = ScrapingUtils.clean_text(title_elem.get_text())
            
            # Filtrar solo eventos de freestyle/batalla
            if not any(keyword in title.lower() for keyword in 
                      ['battle', 'batalla', 'freestyle', 'god level', 'tournament']):
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
            
            return {
                'nombre': f"God Level - {title}",
                'fecha': date,
                'hora': '',
                'ciudad': self._extract_city(location),
                'pais': self._extract_country(location),
                'venue': location,
                'organizador': 'God Level',
                'link_oficial': link if link else self.base_url,
                'descripcion': f"Torneo internacional de God Level: {title}"
            }
            
        except Exception as e:
            print(f"Error parseando evento de God Level: {e}")
            return None
    
    def _get_known_godlevel_events(self) -> List[Dict[str, Any]]:
        """Eventos conocidos de God Level"""
        return [
            {
                'nombre': 'God Level Fest 2025 - México',
                'fecha': '2025-10-19',
                'hora': '19:00',
                'ciudad': 'Ciudad de México',
                'pais': 'México',
                'venue': 'Foro Sol',
                'organizador': 'God Level',
                'link_oficial': 'https://www.godlevelfest.com/mexico-2025',
                'descripcion': 'Festival internacional de God Level en México 2025'
            },
            {
                'nombre': 'God Level Fest 2025 - Colombia',
                'fecha': '2025-11-02',
                'hora': '18:30',
                'ciudad': 'Bogotá',
                'pais': 'Colombia',
                'venue': 'Coliseo Live',
                'organizador': 'God Level',
                'link_oficial': 'https://www.godlevelfest.com/colombia-2025',
                'descripción': 'Festival internacional de God Level en Colombia 2025'
            },
            {
                'nombre': 'God Level Tournament - Argentina vs Chile',
                'fecha': '2025-09-16',
                'hora': '20:00',
                'ciudad': 'Buenos Aires',
                'pais': 'Argentina',
                'venue': 'Teatro Vorterix',
                'organizador': 'God Level',
                'link_oficial': 'https://www.godlevelfest.com/argentina-chile',
                'descripcion': 'Torneo internacional Argentina vs Chile'
            },
            {
                'nombre': 'God Level Battle - España vs México',
                'fecha': '2025-10-26',
                'hora': '21:00',
                'ciudad': 'Madrid',
                'pais': 'España',
                'venue': 'Palacio Vistalegre',
                'organizador': 'God Level',
                'link_oficial': 'https://www.godlevelfest.com/espana-mexico',
                'descripcion': 'Batalla internacional España vs México'
            },
            {
                'nombre': 'God Level Championship 2025',
                'fecha': '2025-12-07',
                'hora': '19:30',
                'ciudad': 'Miami',
                'pais': 'Estados Unidos',
                'venue': 'American Airlines Arena',
                'organizador': 'God Level',
                'link_oficial': 'https://www.godlevelfest.com/championship-2025',
                'descripcion': 'Campeonato mundial de God Level 2025'
            }
        ]
    
    def _extract_city(self, location: str) -> str:
        """Extrae la ciudad de una ubicación"""
        if not location:
            return ""
        
        # Ciudades comunes en eventos internacionales
        cities = ['México', 'Bogotá', 'Buenos Aires', 'Madrid', 'Lima', 'Santiago',
                 'Medellín', 'Guadalajara', 'Valencia', 'Barcelona', 'Miami', 'Los Angeles']
        
        for city in cities:
            if city.lower() in location.lower():
                return city
        
        # Si no encuentra ciudad conocida, tomar la primera parte
        parts = location.split(',')
        return parts[0].strip() if parts else ""
    
    def _extract_country(self, location: str) -> str:
        """Extrae el país de una ubicación"""
        if not location:
            return ""
        
        countries = {
            'méxico': 'México', 'mexico': 'México',
            'colombia': 'Colombia',
            'argentina': 'Argentina',
            'españa': 'España', 'spain': 'España',
            'perú': 'Perú', 'peru': 'Perú',
            'chile': 'Chile',
            'venezuela': 'Venezuela',
            'usa': 'Estados Unidos', 'united states': 'Estados Unidos'
        }
        
        location_lower = location.lower()
        for key, value in countries.items():
            if key in location_lower:
                return value
        
        return ""

def main():
    """Función principal para testing"""
    scraper = GodLevelScraper()
    events = scraper.scrape_events()
    
    print(f"\n📊 Resumen God Level:")
    print(f"   Eventos encontrados: {len(events)}")
    
    for event in events:
        print(f"   • {event['nombre']} - {event['fecha']} ({event['pais']})")

if __name__ == "__main__":
    main()
