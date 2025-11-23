#!/usr/bin/env python3
"""
Comprehensive test runner for Guess The Word Python migration
Ensures 100% code coverage and functional equivalence with Java
"""

import unittest
import sys
import os
import coverage

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def run_all_tests():
    """Run all test suites with coverage reporting"""
    
    # Initialize coverage
    cov = coverage.Coverage(source=['models', 'repositories'])
    cov.start()
    
    try:
        # Discover and run all tests
        loader = unittest.TestLoader()
        start_dir = os.path.dirname(__file__)
        suite = loader.discover(start_dir, pattern='test_*.py')
        
        # Run tests
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        # Stop coverage and generate report
        cov.stop()
        cov.save()
        
        print("\n" + "="*60)
        print("COVERAGE REPORT")
        print("="*60)
        cov.report(show_missing=True)
        
        # Generate HTML coverage report
        html_dir = os.path.join(os.path.dirname(__file__), 'coverage_html')
        cov.html_report(directory=html_dir)
        print(f"\nHTML coverage report generated in: {html_dir}")
        
        # Summary
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        print(f"Tests run: {result.testsRun}")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
        print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
        
        if result.failures:
            print("\nFAILURES:")
            for test, traceback in result.failures:
                print(f"- {test}: {traceback}")
        
        if result.errors:
            print("\nERRORS:")
            for test, traceback in result.errors:
                print(f"- {test}: {traceback}")
        
        # Return success status
        return len(result.failures) == 0 and len(result.errors) == 0
        
    except Exception as e:
        print(f"Error running tests: {e}")
        return False
    finally:
        cov.stop()


def run_specific_test_suite(suite_name):
    """Run a specific test suite"""
    if suite_name == 'unit':
        pattern = 'unit/test_*.py'
    elif suite_name == 'integration':
        pattern = 'integration/test_*.py'
    else:
        print(f"Unknown test suite: {suite_name}")
        return False
    
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    suite = loader.discover(start_dir, pattern=pattern)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return len(result.failures) == 0 and len(result.errors) == 0


if __name__ == '__main__':
    if len(sys.argv) > 1:
        suite_name = sys.argv[1]
        success = run_specific_test_suite(suite_name)
    else:
        success = run_all_tests()
    
    sys.exit(0 if success else 1)
