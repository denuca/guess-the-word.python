import pytest
import time
import statistics
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from mock_flask_app import create_test_app


class TestResponseTimes:
    """Response time performance benchmarks"""
    
    @pytest.fixture
    def client(self):
        """Test client"""
        app = create_test_app({'TESTING': True})
        return app.test_client()
    
    def test_home_page_response_time(self, client):
        """Test home page loads quickly"""
        times = []
        
        for _ in range(10):
            start = time.time()
            response = client.get('/')
            end = time.time()
            
            assert response.status_code == 200
            times.append(end - start)
        
        avg_time = statistics.mean(times)
        max_time = max(times)
        
        assert avg_time < 0.05, f"Average response time {avg_time:.3f}s too slow"
        assert max_time < 0.1, f"Max response time {max_time:.3f}s too slow"
    
    def test_game_start_performance(self, client):
        """Test game start endpoint performance"""
        times = []
        
        for level in ['EASY', 'MEDIUM', 'HARD'] * 5:
            start = time.time()
            response = client.post('/game/start', data={'level': level})
            end = time.time()
            
            assert response.status_code == 200
            times.append(end - start)
        
        avg_time = statistics.mean(times)
        p95_time = statistics.quantiles(times, n=20)[18]  # 95th percentile
        
        assert avg_time < 0.02, f"Average game start time {avg_time:.3f}s too slow"
        assert p95_time < 0.05, f"95th percentile time {p95_time:.3f}s too slow"
    
    def test_guess_submission_performance(self, client):
        """Test guess submission performance"""
        # Start a game first
        client.post('/game/start', data={'level': 'MEDIUM'})
        
        times = []
        guesses = ['ANIMAL', 'BAKERY', 'PYTHON', 'QUAINT', 'RHYTHM'] * 3
        
        for guess in guesses:
            start = time.time()
            response = client.post('/game/guess', data={'guess': guess})
            end = time.time()
            
            assert response.status_code == 200
            times.append(end - start)
        
        avg_time = statistics.mean(times)
        max_time = max(times)
        
        assert avg_time < 0.01, f"Average guess time {avg_time:.3f}s too slow"
        assert max_time < 0.02, f"Max guess time {max_time:.3f}s too slow"
    
    def test_status_endpoint_performance(self, client):
        """Test game status endpoint performance"""
        # Start game for active status
        client.post('/game/start', data={'level': 'MEDIUM'})
        
        times = []
        
        for _ in range(20):
            start = time.time()
            response = client.get('/game/status')
            end = time.time()
            
            assert response.status_code == 200
            times.append(end - start)
        
        avg_time = statistics.mean(times)
        
        assert avg_time < 0.005, f"Status endpoint too slow: {avg_time:.3f}s"
