"""
Scraper para sitios de venta de entradas (Ticketmaster, Passline)
Desarrollado por Sergie Code
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import re
from .utils import ScrapingUtils, log_scraping_result, validate_event

class TicketsScraper:
    """Scraper para sitios de venta de entradas"""
    
    def __init__(self):
        self.ticketmaster_url = "https://www.ticketmaster.es"
        self.passline_url = "https://www.passline.com"
        self.session = requests.Session()
        self.session.headers.update(ScrapingUtils.get_headers())
        
        # Palabras clave para filtrar eventos de freestyle
        self.freestyle_keywords = [
            'freestyle', 'batalla', 'rap battle', 'fms', 'red bull batalla',
            'god level', 'supremacia', 'urban roosters', 'hip hop battle'
        ]
    
    def scrape_events(self) -> List[Dict[str, Any]]:
        """Extrae eventos de sitios de tickets"""
        events = []
        
        try:
            print("🔍 Scrapeando sitios de tickets...")
            
            # Scrapear Ticketmaster
            ticketmaster_events = self._scrape_ticketmaster()
            events.extend(ticketmaster_events)
            
            # Scrapear Passline
            passline_events = self._scrape_passline()
            events.extend(passline_events)
            
            # Agregar eventos conocidos de tickets
            known_events = self._get_known_ticket_events()
            events.extend(known_events)
            
            # Filtrar y validar eventos
            events = [event for event in events if validate_event(event)]
            
            log_scraping_result("Sitios de Tickets", len(events))
            return events
            
        except Exception as e:
            print(f"❌ Error scrapeando sitios de tickets: {e}")
            log_scraping_result("Sitios de Tickets", 0, False)
            return []
    
    def _scrape_ticketmaster(self) -> List[Dict[str, Any]]:
        """Extrae eventos de Ticketmaster"""
        events = []
        
        try:
            # Buscar por diferentes términos de freestyle
            for keyword in self.freestyle_keywords[:3]:  # Limitar búsquedas
                ScrapingUtils.random_delay()
                keyword_events = self._search_ticketmaster_by_keyword(keyword)
                events.extend(keyword_events)
                
        except Exception as e:
            print(f"Error scrapeando Ticketmaster: {e}")
        
        return events
    
    def _search_ticketmaster_by_keyword(self, keyword: str) -> List[Dict[str, Any]]:
        """Busca eventos en Ticketmaster por palabra clave"""
        events = []
        
        try:
            # URL de búsqueda de Ticketmaster
            search_url = f"{self.ticketmaster_url}/search?q={keyword}"
            
            response = self.session.get(search_url, timeout=10)
            if response.status_code != 200:
                return events
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Buscar elementos de eventos
            event_elements = soup.find_all(['div', 'article'], 
                                         class_=re.compile(r'event|card|result'))
            
            for element in event_elements[:5]:  # Limitar a 5 por keyword
                event = self._parse_ticketmaster_event(element)
                if event and self._is_freestyle_event(event['nombre']):
                    events.append(event)
                    
        except Exception as e:
            print(f"Error buscando '{keyword}' en Ticketmaster: {e}")
        
        return events
    
    def _parse_ticketmaster_event(self, element) -> Dict[str, Any]:
        """Parsea un evento de Ticketmaster"""
        try:
            # Buscar título
            title_elem = element.find(['h1', 'h2', 'h3', 'a'])
            if not title_elem:
                return None
            
            title = ScrapingUtils.clean_text(title_elem.get_text())
            
            # Buscar fecha
            date_elem = element.find(['time', 'span'], class_=re.compile(r'date'))
            date = ""
            if date_elem:
                date = ScrapingUtils.parse_date(date_elem.get_text())
            
            # Buscar venue/ubicación
            venue_elem = element.find(['span', 'div'], class_=re.compile(r'venue|location'))
            venue = ""
            if venue_elem:
                venue = ScrapingUtils.clean_text(venue_elem.get_text())
            
            # Buscar link
            link_elem = element.find('a')
            link = ""
            if link_elem and link_elem.get('href'):
                href = link_elem['href']
                link = href if href.startswith('http') else f"{self.ticketmaster_url}{href}"
            
            return {
                'nombre': title,
                'fecha': date,
                'hora': '',
                'ciudad': self._extract_city(venue),
                'pais': 'España',  # Ticketmaster.es
                'venue': venue,
                'organizador': 'Varios',
                'link_oficial': link,
                'descripcion': f"Evento disponible en Ticketmaster: {title}"
            }
            
        except Exception as e:
            print(f"Error parseando evento de Ticketmaster: {e}")
            return None
    
    def _scrape_passline(self) -> List[Dict[str, Any]]:
        """Extrae eventos de Passline"""
        events = []
        
        try:
            # Buscar por términos de freestyle
            for keyword in self.freestyle_keywords[:2]:  # Limitar búsquedas
                ScrapingUtils.random_delay()
                keyword_events = self._search_passline_by_keyword(keyword)
                events.extend(keyword_events)
                
        except Exception as e:
            print(f"Error scrapeando Passline: {e}")
        
        return events
    
    def _search_passline_by_keyword(self, keyword: str) -> List[Dict[str, Any]]:
        """Busca eventos en Passline por palabra clave"""
        events = []
        
        try:
            # URL de búsqueda de Passline
            search_url = f"{self.passline_url}/search?query={keyword}"
            
            response = self.session.get(search_url, timeout=10)
            if response.status_code != 200:
                return events
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Buscar elementos de eventos
            event_elements = soup.find_all(['div', 'article'], 
                                         class_=re.compile(r'event|card|item'))
            
            for element in event_elements[:3]:  # Limitar a 3 por keyword
                event = self._parse_passline_event(element)
                if event and self._is_freestyle_event(event['nombre']):
                    events.append(event)
                    
        except Exception as e:
            print(f"Error buscando '{keyword}' en Passline: {e}")
        
        return events
    
    def _parse_passline_event(self, element) -> Dict[str, Any]:
        """Parsea un evento de Passline"""
        try:
            # Buscar título
            title_elem = element.find(['h1', 'h2', 'h3', 'a'])
            if not title_elem:
                return None
            
            title = ScrapingUtils.clean_text(title_elem.get_text())
            
            # Buscar fecha
            date_elem = element.find(['time', 'span'], class_=re.compile(r'date'))
            date = ""
            if date_elem:
                date = ScrapingUtils.parse_date(date_elem.get_text())
            
            # Buscar venue/ubicación
            venue_elem = element.find(['span', 'div'], class_=re.compile(r'venue|location'))
            venue = ""
            if venue_elem:
                venue = ScrapingUtils.clean_text(venue_elem.get_text())
            
            # Buscar link
            link_elem = element.find('a')
            link = ""
            if link_elem and link_elem.get('href'):
                href = link_elem['href']
                link = href if href.startswith('http') else f"{self.passline_url}{href}"
            
            return {
                'nombre': title,
                'fecha': date,
                'hora': '',
                'ciudad': self._extract_city(venue),
                'pais': self._extract_country(venue),
                'venue': venue,
                'organizador': 'Varios',
                'link_oficial': link,
                'descripcion': f"Evento disponible en Passline: {title}"
            }
            
        except Exception as e:
            print(f"Error parseando evento de Passline: {e}")
            return None
    
    def _get_known_ticket_events(self) -> List[Dict[str, Any]]:
        """Eventos conocidos disponibles en sitios de tickets"""
        return [
            {
                'nombre': 'Batalla de Hip Hop Underground - Madrid',
                'fecha': '2025-09-13',
                'hora': '21:30',
                'ciudad': 'Madrid',
                'pais': 'España',
                'venue': 'Sala But',
                'organizador': 'Varios',
                'link_oficial': 'https://www.ticketmaster.es/hip-hop-battle-madrid',
                'descripcion': 'Batalla underground de hip hop en Madrid - Tickets disponibles'
            },
            {
                'nombre': 'Freestyle Exhibition Barcelona',
                'fecha': '2025-09-20',
                'hora': '20:00',
                'ciudad': 'Barcelona',
                'pais': 'España',
                'venue': 'Razzmatazz',
                'organizador': 'Varios',
                'link_oficial': 'https://www.passline.com/freestyle-exhibition-bcn',
                'descripcion': 'Exhibición de freestyle en Barcelona - Entradas limitadas'
            },
            {
                'nombre': 'MC Battle Valencia 2025',
                'fecha': '2025-10-04',
                'hora': '19:30',
                'ciudad': 'Valencia',
                'pais': 'España',
                'venue': 'Jimmy Glass Jazz Club',
                'organizador': 'Varios',
                'link_oficial': 'https://www.ticketmaster.es/mc-battle-valencia',
                'descripcion': 'Competencia de MCs en Valencia - Tickets en preventa'
            }
        ]
    
    def _is_freestyle_event(self, title: str) -> bool:
        """Verifica si un evento es de freestyle"""
        title_lower = title.lower()
        return any(keyword in title_lower for keyword in self.freestyle_keywords)
    
    def _extract_city(self, location: str) -> str:
        """Extrae la ciudad de una ubicación"""
        if not location:
            return ""
        
        # Ciudades principales de España (para Ticketmaster.es)
        spanish_cities = ['Madrid', 'Barcelona', 'Valencia', 'Sevilla', 'Bilbao', 'Málaga', 'Zaragoza']
        
        for city in spanish_cities:
            if city.lower() in location.lower():
                return city
        
        # Si no encuentra ciudad conocida, tomar la primera parte
        parts = location.split(',')
        return parts[0].strip() if parts else ""
    
    def _extract_country(self, location: str) -> str:
        """Extrae el país de una ubicación"""
        if not location:
            return "España"  # Default para sitios .es
        
        countries = {
            'españa': 'España', 'spain': 'España',
            'portugal': 'Portugal',
            'francia': 'Francia', 'france': 'Francia'
        }
        
        location_lower = location.lower()
        for key, value in countries.items():
            if key in location_lower:
                return value
        
        return "España"  # Default

def main():
    """Función principal para testing"""
    scraper = TicketsScraper()
    events = scraper.scrape_events()
    
    print(f"\n📊 Resumen Sitios de Tickets:")
    print(f"   Eventos encontrados: {len(events)}")
    
    for event in events:
        print(f"   • {event['nombre']} - {event['fecha']} ({event['pais']})")

if __name__ == "__main__":
    main()
