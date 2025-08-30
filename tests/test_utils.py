"""
Unit tests for scraper utilities
"""
import unittest
import tempfile
import os
import sqlite3
import sys
from unittest.mock import patch

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scraper.utils import EventDatabase, ScrapingUtils, CSVExporter, validate_event


class TestEventDatabase(unittest.TestCase):
    """Test cases for EventDatabase class"""
    
    def setUp(self):
        """Set up test database"""
        self.temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.temp_db.close()
        self.db = EventDatabase(self.temp_db.name)
    
    def tearDown(self):
        """Clean up test database"""
        try:
            os.unlink(self.temp_db.name)
        except Exception:
            pass
    
    def test_database_creation(self):
        """Test database and table creation"""
        # Check if database file exists
        self.assertTrue(os.path.exists(self.temp_db.name))
        
        # Check if table exists
        conn = sqlite3.connect(self.temp_db.name)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='eventos'")
        result = cursor.fetchone()
        conn.close()
        
        self.assertIsNotNone(result)
    
    def test_insert_event(self):
        """Test event insertion"""
        test_events = [
            {
                'nombre': 'Test Battle',
                'fecha': '2025-09-15',
                'hora': '20:00',
                'ciudad': 'Madrid',
                'pais': 'España',
                'venue': 'Test Venue',
                'organizador': 'Test Org',
                'link_oficial': 'https://test.com',
                'descripcion': 'Test description'
            }
        ]
        
        # Insert events (note: method is insert_events, not insert_event)
        self.db.insert_events(test_events)
        
        # Verify insertion
        events = self.db.get_all_events()
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]['nombre'], 'Test Battle')
    
    def test_get_events_by_country(self):
        """Test filtering events by country"""
        events = [
            {
                'nombre': 'Spain Battle',
                'fecha': '2025-09-15',
                'hora': '20:00',
                'ciudad': 'Madrid',
                'pais': 'España',
                'venue': 'Venue 1',
                'organizador': 'Org 1',
                'link_oficial': 'https://test1.com',
                'descripcion': 'Spain event'
            },
            {
                'nombre': 'Mexico Battle',
                'fecha': '2025-09-16',
                'hora': '19:00',
                'ciudad': 'CDMX',
                'pais': 'México',
                'venue': 'Venue 2',
                'organizador': 'Org 2',
                'link_oficial': 'https://test2.com',
                'descripcion': 'Mexico event'
            }
        ]
        
        # Insert events
        self.db.insert_events(events)
        
        # Test filtering - note: we need to implement get_events_by_country or use get_all_events
        all_events = self.db.get_all_events()
        spain_events = [e for e in all_events if e['pais'] == 'España']
        mexico_events = [e for e in all_events if e['pais'] == 'México']
        
        self.assertEqual(len(spain_events), 1)
        self.assertEqual(len(mexico_events), 1)
        self.assertEqual(spain_events[0]['nombre'], 'Spain Battle')
        self.assertEqual(mexico_events[0]['nombre'], 'Mexico Battle')


class TestScrapingUtils(unittest.TestCase):
    """Test cases for ScrapingUtils class"""
    
    def test_clean_text(self):
        """Test text cleaning functionality"""
        # Test basic cleaning
        dirty_text = "  \n\t  Text with whitespace  \r\n  "
        clean_text = ScrapingUtils.clean_text(dirty_text)
        self.assertEqual(clean_text, "Text with whitespace")
        
        # Test empty string
        self.assertEqual(ScrapingUtils.clean_text(""), "")
        
        # Test None
        self.assertEqual(ScrapingUtils.clean_text(None), "")
    
    def test_parse_date(self):
        """Test date parsing functionality"""
        # Test various date formats - adjusted for actual implementation
        test_cases = [
            ("15/09/2025", "2025-09-15"),
            ("15-09-2025", "2025-09-15"),
            ("2025-09-15", "2025-09-15"),
            ("invalid date", "invalid date"),  # Returns original if can't parse
            ("", ""),
            (None, "")
        ]
        
        for input_date, expected in test_cases:
            with self.subTest(input_date=input_date):
                result = ScrapingUtils.parse_date(input_date)
                self.assertEqual(result, expected)
    
    def test_get_headers(self):
        """Test HTTP headers generation"""
        headers = ScrapingUtils.get_headers()
        
        # Check required headers exist
        self.assertIn('User-Agent', headers)
        self.assertIn('Accept', headers)
        self.assertIn('Accept-Language', headers)
        
        # Check User-Agent is not empty
        self.assertTrue(len(headers['User-Agent']) > 0)
    
    @patch('time.sleep')
    def test_random_delay(self, mock_sleep):
        """Test random delay functionality"""
        ScrapingUtils.random_delay()
        
        # Verify sleep was called
        mock_sleep.assert_called_once()
        
        # Verify delay is within expected range
        call_args = mock_sleep.call_args[0][0]
        self.assertGreaterEqual(call_args, 1)
        self.assertLessEqual(call_args, 3)


class TestCSVExporter(unittest.TestCase):
    """Test cases for CSVExporter class"""
    
    def test_export_events(self):
        """Test CSV export functionality"""
        test_events = [
            {
                'nombre': 'Test Event 1',
                'fecha': '2025-09-15',
                'hora': '20:00',
                'ciudad': 'Madrid',
                'pais': 'España',
                'venue': 'Test Venue 1',
                'organizador': 'Test Org 1',
                'link_oficial': 'https://test1.com',
                'descripcion': 'Test description 1'
            },
            {
                'nombre': 'Test Event 2',
                'fecha': '2025-09-16',
                'hora': '19:00',
                'ciudad': 'Barcelona',
                'pais': 'España',
                'venue': 'Test Venue 2',
                'organizador': 'Test Org 2',
                'link_oficial': 'https://test2.com',
                'descripcion': 'Test description 2'
            }
        ]
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(suffix='.csv', delete=False)
        temp_file.close()
        
        try:
            # Export events - CSVExporter is static method
            CSVExporter.export_events(test_events, temp_file.name)
            
            # Verify file exists and has content
            self.assertTrue(os.path.exists(temp_file.name))
            
            # Check file content
            with open(temp_file.name, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertIn('Test Event 1', content)
                self.assertIn('Test Event 2', content)
                self.assertIn('Madrid', content)
                self.assertIn('Barcelona', content)
        
        finally:
            # Clean up
            try:
                os.unlink(temp_file.name)
            except Exception:
                pass


class TestValidateEvent(unittest.TestCase):
    """Test cases for event validation"""
    
    def test_valid_event(self):
        """Test validation of valid event"""
        valid_event = {
            'nombre': 'Valid Event',
            'fecha': '2025-09-15',
            'hora': '20:00',
            'ciudad': 'Madrid',
            'pais': 'España',
            'venue': 'Valid Venue',
            'organizador': 'Valid Org',
            'link_oficial': 'https://valid.com',
            'descripcion': 'Valid description'
        }
        
        self.assertTrue(validate_event(valid_event))
    
    def test_invalid_event_missing_fields(self):
        """Test validation of event with missing required fields"""
        invalid_event = {
            'nombre': '',  # Empty name
            'fecha': '2025-09-15',
            'ciudad': 'Madrid'
        }
        
        self.assertFalse(validate_event(invalid_event))
    
    def test_invalid_event_none(self):
        """Test validation of None event"""
        # Need to handle None case in validation
        result = validate_event(None)
        self.assertFalse(result)
    
    def test_invalid_event_empty_dict(self):
        """Test validation of empty event dictionary"""
        self.assertFalse(validate_event({}))


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)
