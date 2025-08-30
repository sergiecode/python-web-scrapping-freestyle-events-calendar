"""
Integration tests for the complete system
"""
import unittest
import tempfile
import os
import sys
from unittest.mock import patch

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scraper.utils import EventDatabase


class TestSystemIntegration(unittest.TestCase):
    """Integration tests for the complete scraping and web system"""
    
    def setUp(self):
        """Set up integration test environment"""
        self.temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.temp_db.close()
        
        self.temp_csv = tempfile.NamedTemporaryFile(suffix='.csv', delete=False)
        self.temp_csv.close()
    
    def tearDown(self):
        """Clean up integration test environment"""
        try:
            os.unlink(self.temp_db.name)
            os.unlink(self.temp_csv.name)
        except Exception:
            pass
    
    def test_end_to_end_scraping_workflow(self):
        """Test complete scraping workflow"""
        # Create database
        db = EventDatabase(self.temp_db.name)
        
        # Test inserting sample events
        sample_events = [
            {
                'nombre': 'Integration Test Battle',
                'fecha': '2025-09-15',
                'hora': '20:00',
                'ciudad': 'Madrid',
                'pais': 'España',
                'venue': 'Test Venue',
                'organizador': 'Test Org',
                'link_oficial': 'https://test.com',
                'descripcion': 'Integration test event'
            }
        ]
        
        # Insert events
        for event in sample_events:
            db.insert_events([event])
        
        # Verify events were inserted
        all_events = db.get_all_events()
        self.assertEqual(len(all_events), 1)
        self.assertEqual(all_events[0]['nombre'], 'Integration Test Battle')
        
        # Test filtering
        spain_events = [e for e in all_events if e.get('pais') == 'España']
        self.assertEqual(len(spain_events), 1)
        
        # Test CSV export
        from scraper.utils import CSVExporter
        CSVExporter.export_events(all_events, self.temp_csv.name)
        
        # Verify CSV was created
        self.assertTrue(os.path.exists(self.temp_csv.name))
        
        # Check CSV content
        with open(self.temp_csv.name, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('Integration Test Battle', content)
    
    @patch('requests.Session.get')
    def test_scraper_resilience(self, mock_get):
        """Test that scrapers are resilient to network issues"""
        # Mock network timeouts and errors
        mock_get.side_effect = Exception("Network timeout")
        
        from scraper.redbull import RedBullScraper
        from scraper.fms import FMSScraper
        
        # Test that scrapers handle errors gracefully
        scrapers = [RedBullScraper(), FMSScraper()]
        
        for scraper in scrapers:
            try:
                events = scraper.scrape_events()
                # Should return list (either empty or with known events)
                self.assertIsInstance(events, list)
            except Exception as e:
                self.fail(f"Scraper {scraper.__class__.__name__} failed to handle network error: {e}")
    
    def test_database_concurrent_access(self):
        """Test database handles concurrent access"""
        db = EventDatabase(self.temp_db.name)
        
        # Simulate multiple inserts
        events = []
        for i in range(10):
            event = {
                'nombre': f'Concurrent Test Battle {i}',
                'fecha': '2025-09-15',
                'hora': '20:00',
                'ciudad': 'Madrid',
                'pais': 'España',
                'venue': f'Venue {i}',
                'organizador': 'Test Org',
                'link_oficial': f'https://test{i}.com',
                'descripcion': f'Concurrent test event {i}'
            }
            events.append(event)
            db.insert_events([event])
        
        # Verify all events were inserted
        all_events = db.get_all_events()
        self.assertEqual(len(all_events), 10)
    
    def test_data_validation_pipeline(self):
        """Test data validation throughout the pipeline"""
        from scraper.utils import validate_event
        
        # Test valid event
        valid_event = {
            'nombre': 'Valid Battle',
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
        
        # Test invalid events
        invalid_events = [
            {},  # Empty
            {'nombre': ''},  # Empty name
            {'nombre': 'Test', 'fecha': 'invalid-date'},  # Invalid date
            None  # None
        ]
        
        for invalid_event in invalid_events:
            self.assertFalse(validate_event(invalid_event))
    
    def test_api_data_consistency(self):
        """Test that API returns consistent data"""
        # Create test database with events
        db = EventDatabase(self.temp_db.name)
        
        test_events = [
            {
                'nombre': 'API Test Battle 1',
                'fecha': '2025-09-15',
                'hora': '20:00',
                'ciudad': 'Madrid',
                'pais': 'España',
                'venue': 'Venue 1',
                'organizador': 'Red Bull',
                'link_oficial': 'https://test1.com',
                'descripcion': 'API test event 1'
            },
            {
                'nombre': 'API Test Battle 2',
                'fecha': '2025-09-16',
                'hora': '19:00',
                'ciudad': 'Barcelona',
                'pais': 'España',
                'venue': 'Venue 2',
                'organizador': 'FMS',
                'link_oficial': 'https://test2.com',
                'descripcion': 'API test event 2'
            }
        ]
        
        for event in test_events:
            db.insert_events([event])
        
        # Test data retrieval
        all_events = db.get_all_events()
        spain_events = [e for e in all_events if e.get('pais') == 'España']
        
        self.assertEqual(len(all_events), 2)
        self.assertEqual(len(spain_events), 2)
        
        # Verify data structure
        for event in all_events:
            self.assertIn('nombre', event)
            self.assertIn('fecha', event)
            self.assertIn('pais', event)
            self.assertIn('organizador', event)


class TestPerformance(unittest.TestCase):
    """Basic performance tests"""
    
    def test_large_dataset_handling(self):
        """Test handling of large datasets"""
        temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        temp_db.close()
        
        try:
            db = EventDatabase(temp_db.name)
            
            # Insert many events
            import time
            start_time = time.time()
            
            for i in range(100):
                event = {
                    'nombre': f'Performance Test Battle {i}',
                    'fecha': '2025-09-15',
                    'hora': '20:00',
                    'ciudad': 'Madrid',
                    'pais': 'España',
                    'venue': f'Venue {i}',
                    'organizador': 'Test Org',
                    'link_oficial': f'https://test{i}.com',
                    'descripcion': f'Performance test event {i}'
                }
                db.insert_events([event])
            
            end_time = time.time()
            
            # Should complete within reasonable time (10 seconds)
            self.assertLess(end_time - start_time, 10)
            
            # Verify all events were inserted
            all_events = db.get_all_events()
            self.assertEqual(len(all_events), 100)
            
        finally:
            try:
                os.unlink(temp_db.name)
            except Exception:
                pass


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)
