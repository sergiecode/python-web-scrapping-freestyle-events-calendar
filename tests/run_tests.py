"""
Test runner for Freestyle Events Calendar
Ejecuta todas las pruebas del proyecto usando unittest
"""
import unittest
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

def run_tests():
    """Run all tests"""
    print("🧪 Iniciando pruebas del Freestyle Events Calendar")
    print("=" * 60)
    
    # Discover and run all tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    print(f"✅ Pruebas ejecutadas: {result.testsRun}")
    print(f"❌ Fallos: {len(result.failures)}")
    print(f"⚠️  Errores: {len(result.errors)}")
    
    if result.failures:
        print(f"\n❌ FALLOS ({len(result.failures)}):")
        for test, traceback in result.failures:
            print(f"   • {test}: {traceback.splitlines()[-1]}")
    
    if result.errors:
        print(f"\n⚠️  ERRORES ({len(result.errors)}):")
        for test, traceback in result.errors:
            print(f"   • {test}: {traceback.splitlines()[-1]}")
    
    if result.wasSuccessful():
        print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
        return True
    else:
        print(f"\n💥 {len(result.failures + result.errors)} pruebas fallaron")
        return False

def run_specific_test(test_module):
    """Run a specific test module"""
    print(f"🧪 Ejecutando pruebas de {test_module}")
    print("=" * 60)
    
    # Load specific test module
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName(test_module)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Run specific test
        test_module = sys.argv[1]
        success = run_specific_test(test_module)
    else:
        # Run all tests
        success = run_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)
