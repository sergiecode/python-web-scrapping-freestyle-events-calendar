# Freestyle Events Calendar Scraper

Un proyecto de web scraping desarrollado por **Sergie Code** que extrae eventos de freestyle de múltiples fuentes y los muestra en una interfaz web con calendario.

## 🎯 Características

- **Scraping automatizado** de eventos de freestyle de múltiples fuentes:
  - Red Bull Batalla
  - Urban Roosters (FMS)
  - God Level
  - Supremacía MC
  - Ticketmaster y Passline
- **Base de datos SQLite** para almacenamiento
- **Interfaz web responsiva** con Bootstrap
- **API REST** para acceso a los datos
- **Filtros** por país y organizador
- **Calendario visual** de eventos

## 🛠️ Tecnologías

- **Python 3.8+**
- **Flask** (Backend web)
- **BeautifulSoup + Selenium** (Web scraping)
- **Pandas** (Manipulación de datos)
- **SQLite** (Base de datos)
- **Bootstrap** (Frontend responsivo)

## 📋 Instalación

1. **Clona el repositorio:**
```bash
git clone <repository-url>
cd python-web-scrapping-freestyle-events-calendar
```

2. **Crea un entorno virtual:**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

3. **Instala las dependencias:**
```powershell
pip install -r requirements.txt
```

4. **Ejecuta el scraper inicial:**
```powershell
python scraper/run_all.py
```

5. **Inicia la aplicación web:**
```powershell
python webapp/app.py
```

6. **Abre tu navegador en:** `http://localhost:5000`

## 📁 Estructura del Proyecto

```
python-web-scrapping-freestyle-events-calendar/
├── scraper/
│   ├── __init__.py
│   ├── redbull.py          # Scraper de Red Bull
│   ├── fms.py              # Scraper de Urban Roosters
│   ├── godlevel.py         # Scraper de God Level
│   ├── supremacia.py       # Scraper de Supremacía MC
│   ├── tickets.py          # Scraper de sitios de tickets
│   ├── utils.py            # Utilidades comunes
│   └── run_all.py          # Script principal
├── webapp/
│   ├── app.py              # Aplicación Flask
│   ├── templates/
│   │   └── index.html      # Template principal
│   └── static/
│       └── styles.css      # Estilos CSS
├── data/
│   ├── eventos.csv         # Datos en CSV
│   └── eventos.db          # Base de datos SQLite
├── requirements.txt
├── README.md
└── .gitignore
```

## 🚀 Uso

### Scraping Manual
```powershell
# Ejecutar todos los scrapers
python scraper/run_all.py

# Ejecutar scraper específico
python scraper/redbull.py
python scraper/fms.py
```

### API Endpoints
- `GET /` - Página principal con calendario
- `GET /api/eventos` - Todos los eventos en JSON
- `GET /api/eventos?pais=España` - Filtrar por país
- `GET /api/eventos?organizador=Red Bull` - Filtrar por organizador

### Filtros Disponibles
- **Por país:** España, México, Argentina, Colombia, etc.
- **Por organizador:** Red Bull, Urban Roosters, God Level, Supremacía MC

## 📊 Datos Extraídos

Para cada evento se extrae:
- **Nombre del evento**
- **Fecha y hora**
- **Lugar** (ciudad, país, venue)
- **Organizador**
- **Link oficial**
- **Descripción** (si está disponible)

## 🔄 Automatización

El proyecto incluye un sistema de scraping automatizado que puede configurarse para ejecutarse periódicamente usando `schedule`.

## 🤝 Contribuir

¿Quieres agregar más fuentes de eventos o mejorar el proyecto? ¡Las contribuciones son bienvenidas!

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📺 Sobre el Autor

**Sergie Code** - Software Engineer y educador de programación en YouTube.

- 📸 Instagram: https://www.instagram.com/sergiecode
- 🧑🏼‍💻 LinkedIn: https://www.linkedin.com/in/sergiecode/
- 📽️ Youtube: https://www.youtube.com/@SergieCode
- 😺 Github: https://github.com/sergiecode
- 👤 Facebook: https://www.facebook.com/sergiecodeok
- 🎞️ Tiktok: https://www.tiktok.com/@sergiecode
- 🕊️ Twitter: https://twitter.com/sergiecode
- 🧵 Threads: https://www.threads.net/@sergiecode

## ⚠️ Disclaimer

Este proyecto es solo para fines educativos. Asegúrate de respetar los términos de servicio de las páginas web que scrapeaste y considera implementar delays apropiados entre requests.
