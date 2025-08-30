"""
Unit tests for Flask web application
"""
import unittest
import tempfile
import os
import sys
import json
from unittest.mock import patch

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import the Flask app
from webapp.app import app, EventsAPI


class TestFlaskApp(unittest.TestCase):
    """Test cases for Flask web application"""
    
    def setUp(self):
        """Set up test client"""
        # Create a temporary database for testing
        self.temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.temp_db.close()
        
        # Configure app for testing
        app.config['TESTING'] = True
        app.config['DATABASE'] = self.temp_db.name
        
        # Create test client
        self.client = app.test_client()
        
        # Create test database with sample data
        self._create_test_database()
    
    def tearDown(self):
        """Clean up after tests"""
        try:
            os.unlink(self.temp_db.name)
        except Exception:
            pass
    
    def _create_test_database(self):
        """Create test database with sample events"""
        import sqlite3
        
        conn = sqlite3.connect(self.temp_db.name)
        cursor = conn.cursor()
        
        # Create table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS eventos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                fecha TEXT,
                hora TEXT,
                ciudad TEXT,
                pais TEXT,
                venue TEXT,
                organizador TEXT,
                link_oficial TEXT,
                descripcion TEXT
            )
        ''')
        
        # Insert sample events
        sample_events = [
            ('Test Battle España', '2025-09-15', '20:00', 'Madrid', 'España', 'Test Venue', 'Red Bull', 'https://test.com', 'Test battle'),
            ('Test Battle México', '2025-09-16', '19:00', 'CDMX', 'México', 'Test Arena', 'FMS', 'https://test2.com', 'FMS battle'),
            ('Test Battle Argentina', '2025-09-17', '18:00', 'Buenos Aires', 'Argentina', 'Test Stadium', 'God Level', 'https://test3.com', 'God Level battle')
        ]
        
        cursor.executemany('''
            INSERT INTO eventos (nombre, fecha, hora, ciudad, pais, venue, organizador, link_oficial, descripcion)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_events)
        
        conn.commit()
        conn.close()
    
    def test_home_page(self):
        """Test home page loads correctly"""
        response = self.client.get('/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Freestyle Events Calendar', response.data)
        self.assertIn(b'Sergie Code', response.data)
    
    def test_api_eventos(self):
        """Test events API endpoint"""
        with patch('webapp.app.get_db_connection') as mock_db:
            # Mock database connection
            mock_conn = mock_db.return_value
            mock_cursor = mock_conn.cursor.return_value
            mock_cursor.fetchall.return_value = [
                (1, 'Test Event', '2025-09-15', '20:00', 'Madrid', 'España', 'Test Venue', 'Test Org', 'https://test.com', 'Test desc')
            ]
            mock_cursor.description = [
                ('id',), ('nombre',), ('fecha',), ('hora',), ('ciudad',), 
                ('pais',), ('venue',), ('organizador',), ('link_oficial',), ('descripcion',)
            ]
            
            response = self.client.get('/api/eventos')
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIsInstance(data, list)
            
            if data:
                event = data[0]
                self.assertIn('nombre', event)
                self.assertIn('fecha', event)
                self.assertIn('pais', event)
    
    def test_api_eventos_by_country(self):
        """Test events API with country filter"""
        with patch('webapp.app.get_db_connection') as mock_db:
            # Mock database connection
            mock_conn = mock_db.return_value
            mock_cursor = mock_conn.cursor.return_value
            mock_cursor.fetchall.return_value = [
                (1, 'Spain Event', '2025-09-15', '20:00', 'Madrid', 'España', 'Test Venue', 'Test Org', 'https://test.com', 'Test desc')
            ]
            mock_cursor.description = [
                ('id',), ('nombre',), ('fecha',), ('hora',), ('ciudad',), 
                ('pais',), ('venue',), ('organizador',), ('link_oficial',), ('descripcion',)
            ]
            
            response = self.client.get('/api/eventos?pais=España')
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIsInstance(data, list)
    
    def test_api_eventos_by_organizer(self):
        """Test events API with organizer filter"""
        with patch('webapp.app.get_db_connection') as mock_db:
            # Mock database connection
            mock_conn = mock_db.return_value
            mock_cursor = mock_conn.cursor.return_value
            mock_cursor.fetchall.return_value = [
                (1, 'Red Bull Event', '2025-09-15', '20:00', 'Madrid', 'España', 'Test Venue', 'Red Bull', 'https://test.com', 'Test desc')
            ]
            mock_cursor.description = [
                ('id',), ('nombre',), ('fecha',), ('hora',), ('ciudad',), 
                ('pais',), ('venue',), ('organizador',), ('link_oficial',), ('descripcion',)
            ]
            
            response = self.client.get('/api/eventos?organizador=Red Bull')
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIsInstance(data, list)
    
    def test_api_stats(self):
        """Test statistics API endpoint"""
        with patch('webapp.app.get_db_connection') as mock_db:
            # Mock database connection
            mock_conn = mock_db.return_value
            mock_cursor = mock_conn.cursor.return_value
            
            # Mock different queries for stats
            def side_effect(*args, **kwargs):
                query = args[0] if args else ""
                if "COUNT(*)" in query and "pais" in query:
                    return [('España', 2), ('México', 1)]
                elif "COUNT(*)" in query and "organizador" in query:
                    return [('Red Bull', 2), ('FMS', 1)]
                elif "COUNT(*)" in query:
                    return [(3,)]
                return []
            
            mock_cursor.fetchall.side_effect = side_effect
            mock_cursor.fetchone.side_effect = side_effect
            
            response = self.client.get('/api/stats')
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            
            self.assertIn('total_eventos', data)
            self.assertIn('por_pais', data)
            self.assertIn('por_organizador', data)
    
    def test_favicon(self):
        """Test favicon route"""
        response = self.client.get('/favicon.ico')
        
        # Should return either 200 (if file exists) or 204 (if not found)
        self.assertIn(response.status_code, [200, 204])
    
    def test_404_page(self):
        """Test 404 error page"""
        response = self.client.get('/nonexistent-page')
        
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'404', response.data)
    
    def test_api_error_handling(self):
        """Test API error handling"""
        with patch('webapp.app.get_db_connection') as mock_db:
            # Mock database error
            mock_db.side_effect = Exception("Database error")
            
            response = self.client.get('/api/eventos')
            
            self.assertEqual(response.status_code, 500)
    
    def test_search_functionality(self):
        """Test search functionality in API"""
        with patch('webapp.app.get_db_connection') as mock_db:
            # Mock database connection
            mock_conn = mock_db.return_value
            mock_cursor = mock_conn.cursor.return_value
            mock_cursor.fetchall.return_value = [
                (1, 'Battle Event', '2025-09-15', '20:00', 'Madrid', 'España', 'Test Venue', 'Test Org', 'https://test.com', 'Test desc')
            ]
            mock_cursor.description = [
                ('id',), ('nombre',), ('fecha',), ('hora',), ('ciudad',), 
                ('pais',), ('venue',), ('organizador',), ('link_oficial',), ('descripcion',)
            ]
            
            response = self.client.get('/api/eventos?search=Battle')
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIsInstance(data, list)


class TestDatabaseOperations(unittest.TestCase):
    """Test database operations"""
    
    def setUp(self):
        """Set up test database"""
        self.temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.temp_db.close()
    
    def tearDown(self):
        """Clean up test database"""
        try:
            os.unlink(self.temp_db.name)
        except Exception:
            pass
    
    @patch('webapp.app.DATABASE_PATH')
    def test_get_db_connection(self, mock_db_path):
        """Test database connection"""
        mock_db_path.return_value = self.temp_db.name
        
        # Create a simple database
        import sqlite3
        conn = sqlite3.connect(self.temp_db.name)
        conn.execute('CREATE TABLE test (id INTEGER)')
        conn.close()
        
        # Test connection
        with patch('webapp.app.DATABASE_PATH', self.temp_db.name):
            conn = get_db_connection()
            self.assertIsNotNone(conn)
            conn.close()


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)
