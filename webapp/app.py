"""
Aplicación web Flask para mostrar eventos de freestyle
Desarrollado por Sergie Code
"""

from flask import Flask, render_template, jsonify, request, send_from_directory
import sqlite3
import json
from datetime import datetime
import os
import sys

# Agregar el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scraper.utils import EventDatabase

app = Flask(__name__)
app.config['SECRET_KEY'] = 'freestyle-events-sergie-code-2025'

# Configuración de la base de datos
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'eventos.db')

class EventsAPI:
    """Clase para manejar la API de eventos"""
    
    def __init__(self, db_path):
        self.db_path = db_path
        self.db = EventDatabase(db_path)
    
    def get_all_events(self):
        """Obtiene todos los eventos"""
        return self.db.get_all_events()
    
    def filter_events(self, pais=None, organizador=None, fecha_desde=None, fecha_hasta=None):
        """Filtra eventos según criterios"""
        events = self.get_all_events()
        
        if pais:
            events = [e for e in events if e.get('pais', '').lower() == pais.lower()]
        
        if organizador:
            events = [e for e in events if organizador.lower() in e.get('organizador', '').lower()]
        
        if fecha_desde:
            events = [e for e in events if e.get('fecha', '') >= fecha_desde]
        
        if fecha_hasta:
            events = [e for e in events if e.get('fecha', '') <= fecha_hasta]
        
        return events
    
    def get_stats(self):
        """Obtiene estadísticas de los eventos"""
        events = self.get_all_events()
        
        stats = {
            'total_eventos': len(events),
            'por_organizador': {},
            'por_pais': {},
            'proximos_eventos': 0
        }
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        for event in events:
            # Contar por organizador
            org = event.get('organizador', 'Unknown')
            stats['por_organizador'][org] = stats['por_organizador'].get(org, 0) + 1
            
            # Contar por país
            pais = event.get('pais', 'Unknown')
            stats['por_pais'][pais] = stats['por_pais'].get(pais, 0) + 1
            
            # Contar próximos eventos
            if event.get('fecha', '') >= today:
                stats['proximos_eventos'] += 1
        
        return stats

# Instanciar API
events_api = EventsAPI(DB_PATH)

@app.route('/')
def index():
    """Página principal con calendario de eventos"""
    try:
        # Obtener eventos
        events = events_api.get_all_events()
        
        # Obtener listas únicas para filtros
        paises = sorted(set(e.get('pais', '') for e in events if e.get('pais')))
        organizadores = sorted(set(e.get('organizador', '') for e in events if e.get('organizador')))
        
        # Filtrar eventos próximos (desde hoy)
        today = datetime.now().strftime('%Y-%m-%d')
        proximos_eventos = [e for e in events if e.get('fecha', '') >= today]
        proximos_eventos.sort(key=lambda x: x.get('fecha', ''))
        
        # Obtener estadísticas
        stats = events_api.get_stats()
        
        return render_template('index.html', 
                             events=proximos_eventos,
                             paises=paises,
                             organizadores=organizadores,
                             stats=stats)
    
    except Exception as e:
        print(f"Error en index: {e}")
        return render_template('index.html', 
                             events=[],
                             paises=[],
                             organizadores=[],
                             stats={'total_eventos': 0, 'proximos_eventos': 0},
                             error="Error cargando eventos")

@app.route('/api/eventos')
def api_eventos():
    """API REST para obtener eventos"""
    try:
        # Obtener parámetros de filtro
        pais = request.args.get('pais')
        organizador = request.args.get('organizador')
        fecha_desde = request.args.get('fecha_desde')
        fecha_hasta = request.args.get('fecha_hasta')
        
        # Filtrar eventos
        events = events_api.filter_events(pais, organizador, fecha_desde, fecha_hasta)
        
        # Ordenar por fecha
        events.sort(key=lambda x: x.get('fecha', ''))
        
        return jsonify({
            'success': True,
            'total': len(events),
            'events': events
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'events': []
        }), 500

@app.route('/api/stats')
def api_stats():
    """API para obtener estadísticas"""
    try:
        stats = events_api.get_stats()
        return jsonify({
            'success': True,
            'stats': stats
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/evento/<int:event_id>')
def evento_detalle(event_id):
    """Página de detalle de un evento específico"""
    try:
        events = events_api.get_all_events()
        event = next((e for e in events if e.get('id') == event_id), None)
        
        if not event:
            return "Evento no encontrado", 404
        
        return render_template('evento_detalle.html', event=event)
    
    except Exception as e:
        return f"Error: {e}", 500

@app.route('/favicon.ico')
def favicon():
    """Serve favicon"""
    try:
        return send_from_directory(
            os.path.join(app.root_path, 'static'),
            'favicon.ico',
            mimetype='image/vnd.microsoft.icon'
        )
    except:
        # Si no existe el favicon, devolver una respuesta vacía
        return '', 204

@app.errorhandler(404)
def not_found(error):
    """Página de error 404"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    """Página de error 500"""
    return render_template('500.html'), 500

def create_sample_data():
    """Crea datos de ejemplo si no existen"""
    try:
        events = events_api.get_all_events()
        if not events:
            print("📝 No se encontraron eventos. Ejecuta el scraper primero:")
            print("   python scraper/run_all.py")
            print("\n💡 O ejecuta un scraper individual:")
            print("   python scraper/redbull.py")
    except Exception as e:
        print(f"⚠️ Error accediendo a la base de datos: {e}")
        print("💡 Ejecuta el scraper para crear los datos:")
        print("   python scraper/run_all.py")

if __name__ == '__main__':
    print("🎤 Freestyle Events Calendar - Desarrollado por Sergie Code")
    print("=" * 60)
    
    # Verificar datos
    create_sample_data()
    
    print(f"🌐 Iniciando servidor web...")
    print(f"📂 Base de datos: {DB_PATH}")
    print(f"🔗 URL: http://localhost:5000")
    print("=" * 60)
    
    # Ejecutar aplicación Flask
    app.run(
        debug=True,
        host='localhost',
        port=5000,
        use_reloader=True
    )
