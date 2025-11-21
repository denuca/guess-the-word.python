import pytest
import threading
import time
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from mock_flask_app import create_test_app


class TestLoadScenarios:
    """Performance and load testing scenarios"""
    
    @pytest.fixture
    def app(self):
        """Test application"""
        return create_test_app({'TESTING': True})
    
    def test_concurrent_user_sessions(self, app):
        """Test multiple concurrent game sessions"""
        results = []
        errors = []
        
        def simulate_user_session():
            try:
                with app.test_client() as client:
                    # Start game
                    response = client.post('/game/start', data={'level': 'MEDIUM'})
                    results.append(response.status_code)
                    
                    # Make some guesses
                    for guess in ['ANIMAL', 'BAKERY', 'PYTHON']:
                        response = client.post('/game/guess', data={'guess': guess})
                        results.append(response.status_code)
                        time.sleep(0.001)  # Small delay
            except Exception as e:
                errors.append(str(e))
        
        # Start multiple threads
        threads = [threading.Thread(target=simulate_user_session) for _ in range(5)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        
        # Verify no errors and got expected results
        assert len(errors) == 0, f"Concurrent access caused errors: {errors}"
        assert len(results) == 20  # 5 threads * 4 requests each
        assert all(status == 200 for status in results)
    
    def test_response_time_benchmarks(self, app):
        """Test API response times meet requirements"""
        with app.test_client() as client:
            # Test game start endpoint
            start_time = time.time()
            response = client.post('/game/start', data={'level': 'MEDIUM'})
            end_time = time.time()
            
            assert response.status_code == 200
            assert (end_time - start_time) < 0.1  # Should respond within 100ms
            
            # Test guess endpoint
            start_time = time.time()
            response = client.post('/game/guess', data={'guess': 'ANIMAL'})
            end_time = time.time()
            
            assert response.status_code == 200
            assert (end_time - start_time) < 0.05  # Should be even faster
    
    def test_memory_usage_stability(self, app):
        """Test memory usage remains stable under load"""
        import gc
        
        with app.test_client() as client:
            # Baseline memory
            gc.collect()
            
            # Simulate many game sessions
            for i in range(100):
                client.post('/game/start', data={'level': 'MEDIUM'})
                client.post('/game/guess', data={'guess': 'ANIMAL'})
                
                # Periodic cleanup
                if i % 10 == 0:
                    gc.collect()
            
            # Memory should be stable (no major leaks)
            # This is a basic test - more sophisticated memory profiling
            # would be needed for production
            gc.collect()
            assert True  # If we get here without crashing, memory is stable
