# Freestyle Events Calendar Scraper

Un proyecto de web scraping desarrollado por **Sergie Code** que extrae eventos de freestyle de múltiples fuentes y los muestra en una interfaz web moderna con calendario interactivo.

## 🎯 Características

- **Scraping automatizado** de eventos de freestyle de múltiples fuentes:
  - Red Bull Batalla
  - Urban Roosters (FMS)
  - God Level
  - Supremacía MC
  - Ticketmaster y Passline
- **Base de datos SQLite** con persistencia de datos
- **Interfaz web moderna** con Bootstrap 5 y JavaScript
- **API REST completa** para acceso a los datos
- **Filtros dinámicos** por país, organizador y fecha
- **Calendario visual** de eventos con vista de tarjetas
- **Suite de pruebas completa** con 30 tests automatizados
- **Compatible con Windows/VSCode/PowerShell**
- **Sistema de estadísticas** de eventos

## 🛠️ Tecnologías

- **Python 3.8+**
- **Flask** (Backend web)
- **BeautifulSoup + Selenium** (Web scraping)
- **Pandas** (Manipulación de datos)
- **SQLite** (Base de datos)
- **Bootstrap 5** (Frontend responsivo)
- **JavaScript ES6** (Interactividad)
- **Pytest** (Testing framework)

## 📋 Instalación y Configuración

### Requisitos Previos
- Python 3.8 o superior
- Git
- Google Chrome (para Selenium)

### Pasos de Instalación

1. **Clona el repositorio:**
```powershell
git clone https://github.com/sergiecode/python-web-scrapping-freestyle-events-calendar.git
cd python-web-scrapping-freestyle-events-calendar
```

2. **Crea y activa un entorno virtual:**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

3. **Instala las dependencias:**
```powershell
pip install -r requirements.txt
```

4. **Ejecuta el scraper inicial para poblar la base de datos:**
```powershell
python scraper/run_all.py
```

5. **Inicia la aplicación web:**
```powershell
python webapp/app.py
```

6. **Abre tu navegador en:** `http://localhost:5000`

## ✅ Testing

El proyecto incluye una suite completa de 30 pruebas automatizadas:

### Ejecutar todas las pruebas:
```powershell
pytest tests/ -v
```

### Ejecutar pruebas específicas:
```powershell
# Pruebas de utilidades
pytest tests/test_utils.py -v

# Pruebas de scrapers
pytest tests/test_scrapers.py -v

# Pruebas de integración
pytest tests/test_integration.py -v

# Pruebas de la webapp
pytest tests/test_webapp.py -v
```

### Script de prueba para Windows/PowerShell:
```powershell
# Ejecutar con el script incluido
.\run_tests.ps1
```

5. **Inicia la aplicación web:**
```powershell
python webapp/app.py
```

6. **Abre tu navegador en:** `http://localhost:5000`

## 📁 Estructura del Proyecto

```
python-web-scrapping-freestyle-events-calendar/
├── scraper/                    # Módulos de web scraping
│   ├── __init__.py
│   ├── redbull.py             # Scraper de Red Bull Batalla
│   ├── fms.py                 # Scraper de Urban Roosters (FMS)
│   ├── godlevel.py            # Scraper de God Level
│   ├── supremacia.py          # Scraper de Supremacía MC
│   ├── tickets.py             # Scraper de sitios de tickets
│   ├── utils.py               # Utilidades y funciones comunes
│   └── run_all.py             # Script principal de scraping
├── webapp/                     # Aplicación web Flask
│   ├── app.py                 # Servidor Flask con API REST
│   ├── templates/
│   │   ├── index.html         # Interfaz principal (Bootstrap 5)
│   │   └── api_test.html      # Página de prueba de API
│   └── static/
│       └── styles.css         # Estilos CSS personalizados
├── tests/                      # Suite de pruebas (30 tests)
│   ├── __init__.py
│   ├── test_utils.py          # Pruebas de utilidades
│   ├── test_scrapers.py       # Pruebas de scrapers
│   ├── test_integration.py    # Pruebas de integración
│   └── test_webapp.py         # Pruebas de la webapp
├── data/                       # Datos y base de datos
│   ├── eventos.csv            # Exportación en CSV
│   └── eventos.db             # Base de datos SQLite
├── requirements.txt            # Dependencias de Python
├── run_tests.ps1              # Script de pruebas para PowerShell
├── debug_api.py               # Script de debug de API
├── README.md                  # Este archivo
└── .gitignore                 # Archivos ignorados por Git
```

## 🚀 Uso de la Aplicación

### 🌐 Interfaz Web

La aplicación web ofrece una interfaz moderna y responsiva:

- **Página principal** (`http://localhost:5000`): Vista de tarjetas con todos los eventos
- **Filtros dinámicos**: Por país, organizador y rango de fechas
- **Búsqueda en tiempo real**: Busca eventos por nombre o descripción
- **Vista de estadísticas**: Contador de eventos y distribución por organizador
- **Diseño responsivo**: Compatible con móviles y tablets

### 🔧 Scraping Manual

```powershell
# Ejecutar todos los scrapers
python scraper/run_all.py

# Ejecutar scraper específico
python scraper/redbull.py
python scraper/fms.py
python scraper/godlevel.py
python scraper/supremacia.py
python scraper/tickets.py
```

### 📡 API REST Endpoints

| Endpoint | Método | Descripción | Parámetros |
|----------|--------|-------------|------------|
| `/` | GET | Página principal | - |
| `/api/eventos` | GET | Todos los eventos | `pais`, `organizador` |
| `/api/stats` | GET | Estadísticas de eventos | - |
| `/test` | GET | Página de prueba de API | - |

#### Ejemplos de uso de la API:

```bash
# Todos los eventos
curl http://localhost:5000/api/eventos

# Filtrar por país
curl "http://localhost:5000/api/eventos?pais=España"

# Filtrar por organizador
curl "http://localhost:5000/api/eventos?organizador=Red Bull"

# Múltiples filtros
curl "http://localhost:5000/api/eventos?pais=Argentina&organizador=Urban Roosters"

# Estadísticas
curl http://localhost:5000/api/stats
```

### 🎛️ Filtros Disponibles

- **Por país**: España, México, Argentina, Colombia, Chile, Perú, etc.
- **Por organizador**: Red Bull, Urban Roosters, God Level, Supremacía MC
- **Por fecha**: Eventos próximos, eventos pasados, rango personalizado
- **Búsqueda**: Por nombre del evento o descripción

### 🔍 Debug y Mantenimiento

```powershell
# Verificar funcionamiento de la API
python debug_api.py

# Limpiar y recrear la base de datos
python scraper/utils.py

# Ver logs de la aplicación web
python webapp/app.py  # Los logs aparecen en la consola
```

## 📊 Datos Extraídos

Para cada evento se extrae la siguiente información:

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| **nombre** | Nombre del evento | "Red Bull Batalla Nacional España" |
| **fecha** | Fecha del evento | "2024-03-15" |
| **hora** | Hora del evento | "20:00" |
| **ciudad** | Ciudad donde se realiza | "Madrid" |
| **pais** | País del evento | "España" |
| **venue** | Lugar específico | "Palacio de Deportes" |
| **organizador** | Organizador del evento | "Red Bull" |
| **link** | URL oficial | "https://..." |
| **descripcion** | Descripción del evento | "Batalla nacional de freestyle" |

### 📈 Estadísticas Disponibles

La API de estadísticas (`/api/stats`) proporciona:
- **Total de eventos** en la base de datos
- **Eventos por organizador** (distribución)
- **Eventos por país** (distribución)
- **Eventos próximos** (próximos 30 días)
- **Última actualización** de la base de datos

## 🔄 Automatización y Programación

### Configuración de Scraping Automático

```python
# Ejemplo de automatización con schedule
import schedule
import time
from scraper.run_all import main as run_scrapers

def job():
    print("Ejecutando scraping automático...")
    run_scrapers()
    print("Scraping completado.")

# Ejecutar cada 6 horas
schedule.every(6).hours.do(job)

# Ejecutar diariamente a las 9:00 AM
schedule.every().day.at("09:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
```

### Configuración con Windows Task Scheduler

1. Abre el **Programador de tareas** de Windows
2. Crea una **Nueva tarea básica**
3. Configura el **Desencadenador** (ej: diario)
4. En **Acción**, selecciona "Iniciar un programa"
5. **Programa**: `C:\ruta\a\python.exe`
6. **Argumentos**: `C:\ruta\al\proyecto\scraper\run_all.py`
7. **Iniciar en**: `C:\ruta\al\proyecto\`

## 🛠️ Desarrollo y Personalización

### Agregar un Nuevo Scraper

1. Crea un nuevo archivo en `scraper/nuevo_sitio.py`:

```python
import requests
from bs4 import BeautifulSoup
from .utils import EventsAPI, limpiar_texto

def scraper_nuevo_sitio():
    """Scraper para un nuevo sitio de eventos"""
    api = EventsAPI()
    
    # Tu lógica de scraping aquí
    url = "https://nuevo-sitio.com/eventos"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extraer eventos
    eventos = []
    for evento_elem in soup.find_all('div', class_='evento'):
        evento = {
            'nombre': limpiar_texto(evento_elem.find('h2').text),
            'fecha': evento_elem.find('time').get('datetime'),
            # ... más campos
        }
        eventos.append(evento)
    
    # Guardar en la base de datos
    for evento in eventos:
        api.agregar_evento(**evento)
    
    return len(eventos)

if __name__ == "__main__":
    count = scraper_nuevo_sitio()
    print(f"Scraped {count} eventos from Nuevo Sitio")
```

2. Agrega el import en `scraper/run_all.py`:

```python
from .nuevo_sitio import scraper_nuevo_sitio

def main():
    # ... otros scrapers
    count += scraper_nuevo_sitio()
```

### Personalizar la Interfaz Web

Los archivos principales para personalización:

- **`webapp/templates/index.html`**: Estructura HTML y JavaScript
- **`webapp/static/styles.css`**: Estilos CSS personalizados
- **`webapp/app.py`**: Lógica del servidor y API

## 🐛 Solución de Problemas

### Problemas Comunes

#### La página web no muestra eventos
```powershell
# 1. Verificar que hay eventos en la base de datos
python debug_api.py

# 2. Limpiar caché del navegador (Ctrl + F5)

# 3. Verificar que el servidor está corriendo
curl http://localhost:5000/api/eventos
```

#### Error de ChromeDriver
```powershell
# Instalar/actualizar ChromeDriver
# Descargar desde: https://chromedriver.chromium.org/
# Colocar en PATH o en la carpeta del proyecto
```

#### Error de módulos no encontrados
```powershell
# Asegurarse de que el entorno virtual está activado
venv\Scripts\Activate.ps1

# Reinstalar dependencias
pip install -r requirements.txt
```

#### Pruebas fallan
```powershell
# Ejecutar pruebas individuales para identificar el problema
pytest tests/test_utils.py -v
pytest tests/test_scrapers.py -v

# Verificar entorno de pruebas
python -m pytest --version
```

### Logs y Debug

Para activar logs detallados:

```python
# En webapp/app.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Compatibilidad

- **Sistema Operativo**: Windows 10/11, Linux, macOS
- **Python**: 3.8, 3.9, 3.10, 3.11
- **Navegadores**: Chrome, Firefox, Edge, Safari
- **Terminal**: PowerShell, CMD, Git Bash

## 📝 Changelog

### v2.0.0 (Actual)
- ✅ Suite completa de 30 pruebas automatizadas
- ✅ Interfaz web moderna con Bootstrap 5
- ✅ API REST completa con filtros avanzados
- ✅ Sistema de estadísticas de eventos
- ✅ Compatibilidad completa con Windows/PowerShell
- ✅ Página de debug y pruebas de API
- ✅ Documentación completa actualizada

### v1.0.0 (Anterior)
- Scraping básico de múltiples fuentes
- Base de datos SQLite simple
- Interfaz web básica
- API REST básica

## 🤝 Contribuir

¿Quieres agregar más fuentes de eventos o mejorar el proyecto? ¡Las contribuciones son bienvenidas!

### Proceso de Contribución:

1. **Fork** el proyecto
2. Crea una **rama** para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. **Push** a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un **Pull Request**

### Guías para Contribuir:

- Mantén el código limpio y bien documentado
- Agrega pruebas para nuevas funcionalidades
- Sigue las convenciones de naming existentes
- Actualiza la documentación según sea necesario
- Prueba en Windows/PowerShell antes de enviar PR

### Ideas para Contribuir:

- Nuevos scrapers de sitios de eventos
- Mejoras en la interfaz web
- Optimizaciones de rendimiento
- Integración con APIs externas
- Notificaciones de eventos
- Export a diferentes formatos (JSON, XML, iCal)

## � Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## �📺 Sobre el Autor

**Sergie Code** - Software Engineer y educador de programación en YouTube.

### 🌐 Sígueme en mis redes:

- 📸 **Instagram**: https://www.instagram.com/sergiecode
- 🧑🏼‍💻 **LinkedIn**: https://www.linkedin.com/in/sergiecode/
- 📽️ **YouTube**: https://www.youtube.com/@SergieCode
- 😺 **GitHub**: https://github.com/sergiecode
- 👤 **Facebook**: https://www.facebook.com/sergiecodeok
- 🎞️ **TikTok**: https://www.tiktok.com/@sergiecode
- 🕊️ **Twitter**: https://twitter.com/sergiecode
- 🧵 **Threads**: https://www.threads.net/@sergiecode

### 💡 Otros Proyectos

Visita mi GitHub para más proyectos educativos de programación y desarrollo web.

## ⚠️ Disclaimer

Este proyecto es **solo para fines educativos**. 

**Importante**:
- Respeta los **términos de servicio** de las páginas web que scrapeas
- Implementa **delays apropiados** entre requests para no sobrecargar los servidores
- Considera el **uso ético** del web scraping
- **No uses** este código para fines comerciales sin permisos apropiados
- **Verifica** la legalidad del scraping en tu jurisdicción

---

## 🌟 ¡Apoya el Proyecto!

Si este proyecto te ha sido útil:
- ⭐ **Dale una estrella** en GitHub
- 🐛 **Reporta bugs** o sugiere mejoras
- 🤝 **Contribuye** con código o documentación
- 📢 **Comparte** el proyecto en tus redes

¡Gracias por usar Freestyle Events Calendar Scraper! 🎤🔥
