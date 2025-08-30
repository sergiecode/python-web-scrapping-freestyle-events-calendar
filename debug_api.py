#!/usr/bin/env python3
"""
Test script to debug the EventsAPI
"""

import sys
import os
sys.path.append('.')

# Test the EventsAPI
try:
    from webapp.app import events_api
    print("✅ Successfully imported events_api")
    
    events = events_api.get_all_events()
    print(f"✅ Found {len(events)} events from EventsAPI")
    
    if events:
        print("First few events:")
        for i, event in enumerate(events[:3]):
            titulo = event.get('titulo') or event.get('nombre', 'No title')
            fecha = event.get('fecha', 'No date')
            print(f"  {i+1}. {titulo} - {fecha}")
    else:
        print("❌ No events returned from EventsAPI")
        
    # Test the database directly
    print("\n" + "="*50)
    print("Testing database directly...")
    
    from scraper.utils import EventDatabase
    db_path = 'data/eventos.db'
    if os.path.exists(db_path):
        db = EventDatabase(db_path)
        direct_events = db.get_all_events()
        print(f"✅ Found {len(direct_events)} events from direct DB access")
        
        if direct_events and not events:
            print("❌ ISSUE: Database has events but EventsAPI returns none!")
            print("This suggests a problem with the EventsAPI implementation")
    else:
        print(f"❌ Database file not found: {db_path}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
