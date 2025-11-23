#!/usr/bin/env python3
"""
Integration test runner for Guess The Word Python migration
Tests HTTP endpoints, session management, and performance
"""

import unittest
import sys
import os
import time

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def run_integration_tests():
    """Run all integration test suites"""
    
    print("🧪 Guess The Word Integration Test Suite")
    print("=" * 50)
    
    # Test suites to run
    test_suites = [
        ('API Endpoints', 'integration.test_api_endpoints'),
        ('Session Management', 'integration.test_session_management'), 
        ('Repository Integration', 'integration.test_repository_integration'),
        ('Load Scenarios', 'performance.test_load_scenarios'),
        ('Response Times', 'performance.test_response_times')
    ]
    
    total_tests = 0
    total_failures = 0
    total_errors = 0
    suite_results = []
    
    start_time = time.time()
    
    for suite_name, module_name in test_suites:
        print(f"\n📋 Running {suite_name} Tests...")
        print("-" * 30)
        
        try:
            # Load and run test suite
            loader = unittest.TestLoader()
            suite = loader.loadTestsFromName(module_name)
            
            runner = unittest.TextTestRunner(verbosity=1, stream=sys.stdout)
            result = runner.run(suite)
            
            # Track results
            suite_tests = result.testsRun
            suite_failures = len(result.failures)
            suite_errors = len(result.errors)
            
            total_tests += suite_tests
            total_failures += suite_failures
            total_errors += suite_errors
            
            suite_results.append({
                'name': suite_name,
                'tests': suite_tests,
                'failures': suite_failures,
                'errors': suite_errors,
                'success_rate': ((suite_tests - suite_failures - suite_errors) / suite_tests * 100) if suite_tests > 0 else 0
            })
            
            if suite_failures > 0:
                print(f"❌ {suite_failures} failures in {suite_name}")
            if suite_errors > 0:
                print(f"💥 {suite_errors} errors in {suite_name}")
            if suite_failures == 0 and suite_errors == 0:
                print(f"✅ All {suite_tests} tests passed in {suite_name}")
                
        except Exception as e:
            print(f"💥 Failed to run {suite_name}: {e}")
            suite_results.append({
                'name': suite_name,
                'tests': 0,
                'failures': 0,
                'errors': 1,
                'success_rate': 0
            })
    
    end_time = time.time()
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 INTEGRATION TEST SUMMARY")
    print("=" * 50)
    
    for result in suite_results:
        status = "✅" if result['failures'] == 0 and result['errors'] == 0 else "❌"
        print(f"{status} {result['name']}: {result['tests']} tests, {result['success_rate']:.1f}% success")
    
    print(f"\n📈 Overall Results:")
    print(f"   Total Tests: {total_tests}")
    print(f"   Failures: {total_failures}")
    print(f"   Errors: {total_errors}")
    print(f"   Success Rate: {((total_tests - total_failures - total_errors) / total_tests * 100):.1f}%")
    print(f"   Execution Time: {(end_time - start_time):.2f} seconds")
    
    # Return success status
    return total_failures == 0 and total_errors == 0


def run_specific_suite(suite_name):
    """Run a specific test suite"""
    suite_map = {
        'api': 'integration.test_api_endpoints',
        'session': 'integration.test_session_management',
        'repository': 'integration.test_repository_integration',
        'load': 'performance.test_load_scenarios',
        'performance': 'performance.test_response_times'
    }
    
    if suite_name not in suite_map:
        print(f"Unknown test suite: {suite_name}")
        print(f"Available suites: {', '.join(suite_map.keys())}")
        return False
    
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName(suite_map[suite_name])
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return len(result.failures) == 0 and len(result.errors) == 0


if __name__ == '__main__':
    if len(sys.argv) > 1:
        suite_name = sys.argv[1]
        success = run_specific_suite(suite_name)
    else:
        success = run_integration_tests()
    
    if success:
        print("\n🎉 All integration tests passed! Ready for production.")
    else:
        print("\n⚠️  Some tests failed. Please review and fix issues.")
    
    sys.exit(0 if success else 1)
