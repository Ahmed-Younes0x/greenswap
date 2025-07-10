"""
Load Testing
Testing system performance under various load conditions
"""
import asyncio
import aiohttp
import time
import statistics
from concurrent.futures import ThreadPoolExecutor
import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from locust import HttpUser, task, between

User = get_user_model()

class LoadTestBase(TestCase):
    """Base class for load testing"""
    
    def setUp(self):
        self.client = APIClient()
        self.users = []
        self.tokens = []
        
        # Create test users
        for i in range(10):
            user = User.objects.create_user(
                username=f'loadtest{i}',
                email=f'loadtest{i}@example.com',
                password='TestPass123!'
            )
            token = Token.objects.create(user=user)
            self.users.append(user)
            self.tokens.append(token.key)

class APILoadTests(LoadTestBase):
    """Load tests for API endpoints"""
    
    def test_concurrent_user_registration(self):
        """Test concurrent user registrations"""
        def register_user(user_id):
            client = APIClient()
            data = {
                'username': f'concurrent{user_id}',
                'email': f'concurrent{user_id}@example.com',
                'password': 'TestPass123!',
                'password_confirm': 'TestPass123!',
                'first_name': 'Test',
                'last_name': 'User'
            }
            
            start_time = time.time()
            response = client.post('/api/accounts/register/', data)
            end_time = time.time()
            
            return {
                'status_code': response.status_code,
                'response_time': end_time - start_time,
                'user_id': user_id
            }
        
        # Test with 50 concurrent registrations
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(register_user, i) for i in range(50)]
            results = [future.result() for future in futures]
        
        # Analyze results
        successful_requests = [r for r in results if r['status_code'] == 201]
        response_times = [r['response_time'] for r in results]
        
        self.assertGreaterEqual(len(successful_requests), 45)  # 90% success rate
        self.assertLess(statistics.mean(response_times), 2.0)  # Average < 2 seconds
        self.assertLess(max(response_times), 5.0)  # Max < 5 seconds
    
    def test_concurrent_item_creation(self):
        """Test concurrent item creation"""
        def create_item(token, item_id):
            client = APIClient()
            client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
            
            data = {
                'title': f'Load Test Item {item_id}',
                'description': f'Description {item_id}',
                'category': 1,  # Assuming category exists
                'condition': 'good',
                'location': 'Cairo',
                'price': '100.00'
            }
            
            start_time = time.time()
            response = client.post('/api/items/', data)
            end_time = time.time()
            
            return {
                'status_code': response.status_code,
                'response_time': end_time - start_time,
                'item_id': item_id
            }
        
        # Test with multiple users creating items concurrently
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = []
            for i in range(100):
                token = self.tokens[i % len(self.tokens)]
                futures.append(executor.submit(create_item, token, i))
            
            results = [future.result() for future in futures]
        
        # Analyze results
        successful_requests = [r for r in results if r['status_code'] == 201]
        response_times = [r['response_time'] for r in results]
        
        self.assertGreaterEqual(len(successful_requests), 90)  # 90% success rate
        self.assertLess(statistics.mean(response_times), 1.5)  # Average < 1.5 seconds
    
    def test_high_read_load(self):
        """Test high read load on item list endpoint"""
        def fetch_items(request_id):
            client = APIClient()
            
            start_time = time.time()
            response = client.get('/api/items/')
            end_time = time.time()
            
            return {
                'status_code': response.status_code,
                'response_time': end_time - start_time,
                'request_id': request_id
            }
        
        # Test with 200 concurrent read requests
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(fetch_items, i) for i in range(200)]
            results = [future.result() for future in futures]
        
        # Analyze results
        successful_requests = [r for r in results if r['status_code'] == 200]
        response_times = [r['response_time'] for r in results]
        
        self.assertGreaterEqual(len(successful_requests), 190)  # 95% success rate
        self.assertLess(statistics.mean(response_times), 0.5)  # Average < 0.5 seconds
        self.assertLess(max(response_times), 2.0)  # Max < 2 seconds

class DatabaseLoadTests(LoadTestBase):
    """Load tests for database operations"""
    
    def test_database_connection_pool(self):
        """Test database connection pool under load"""
        from django.db import connection
        
        def execute_query(query_id):
            start_time = time.time()
            
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM auth_user")
                result = cursor.fetchone()
            
            end_time = time.time()
            
            return {
                'result': result[0],
                'response_time': end_time - start_time,
                'query_id': query_id
            }
        
        # Test with 100 concurrent database queries
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(execute_query, i) for i in range(100)]
            results = [future.result() for future in futures]
        
        # All queries should succeed
        self.assertEqual(len(results), 100)
        
        # Response times should be reasonable
        response_times = [r['response_time'] for r in results]
        self.assertLess(statistics.mean(response_times), 0.1)  # Average < 0.1 seconds

class CacheLoadTests(LoadTestBase):
    """Load tests for caching system"""
    
    def test_redis_cache_performance(self):
        """Test Redis cache under high load"""
        from django.core.cache import cache
        
        def cache_operation(operation_id):
            start_time = time.time()
            
            # Set cache value
            cache.set(f'test_key_{operation_id}', f'test_value_{operation_id}', 300)
            
            # Get cache value
            value = cache.get(f'test_key_{operation_id}')
            
            end_time = time.time()
            
            return {
                'success': value is not None,
                'response_time': end_time - start_time,
                'operation_id': operation_id
            }
        
        # Test with 500 concurrent cache operations
        with ThreadPoolExecutor(max_workers=100) as executor:
            futures = [executor.submit(cache_operation, i) for i in range(500)]
            results = [future.result() for future in futures]
        
        # Analyze results
        successful_operations = [r for r in results if r['success']]
        response_times = [r['response_time'] for r in results]
        
        self.assertGreaterEqual(len(successful_operations), 490)  # 98% success rate
        self.assertLess(statistics.mean(response_times), 0.05)  # Average < 0.05 seconds

# Locust load testing classes
class WebsiteUser(HttpUser):
    """Locust user for website load testing"""
    wait_time = between(1, 3)
    
    def on_start(self):
        """Login user at start"""
        response = self.client.post("/api/accounts/login/", json={
            "username": "loadtest1",
            "password": "TestPass123!"
        })
        if response.status_code == 200:
            self.token = response.json()["token"]
            self.client.headers.update({"Authorization": f"Token {self.token}"})
    
    @task(3)
    def view_homepage(self):
        """View homepage"""
        self.client.get("/")
    
    @task(2)
    def browse_items(self):
        """Browse items"""
        self.client.get("/api/items/")
    
    @task(1)
    def search_items(self):
        """Search for items"""
        self.client.get("/api/items/?search=electronics")
    
    @task(1)
    def view_item_detail(self):
        """View item detail"""
        # Get first item
        response = self.client.get("/api/items/")
        if response.status_code == 200:
            items = response.json()["results"]
            if items:
                item_slug = items[0]["slug"]
                self.client.get(f"/api/items/{item_slug}/")
    
    @task(1)
    def create_item(self):
        """Create new item"""
        if hasattr(self, 'token'):
            self.client.post("/api/items/", json={
                "title": "Load Test Item",
                "description": "Test description",
                "category": 1,
                "condition": "good",
                "location": "Cairo",
                "price": "100.00"
            })

class AIServiceUser(HttpUser):
    """Locust user for AI services load testing"""
    wait_time = between(2, 5)
    
    def on_start(self):
        """Login user at start"""
        response = self.client.post("/api/accounts/login/", json={
            "username": "loadtest1",
            "password": "TestPass123!"
        })
        if response.status_code == 200:
            self.token = response.json()["token"]
            self.client.headers.update({"Authorization": f"Token {self.token}"})
    
    @task(2)
    def classify_waste(self):
        """Test waste classification"""
        if hasattr(self, 'token'):
            self.client.post("/api/ai/classify/", json={
                "image_url": "https://example.com/test-image.jpg"
            })
    
    @task(1)
    def chat_with_ai(self):
        """Test AI chat"""
        if hasattr(self, 'token'):
            self.client.post("/api/ai/chat/", json={
                "message": "How do I recycle plastic?",
                "session_id": "load-test-session"
            })

@pytest.mark.asyncio
async class AsyncLoadTests:
    """Asynchronous load tests"""
    
    async def test_async_api_load(self):
        """Test API endpoints with async requests"""
        async def make_request(session, url):
            start_time = time.time()
            async with session.get(url) as response:
                await response.text()
                end_time = time.time()
                return {
                    'status': response.status,
                    'response_time': end_time - start_time
                }
        
        async with aiohttp.ClientSession() as session:
            # Create 1000 concurrent requests
            tasks = []
            for i in range(1000):
                task = make_request(session, 'http://localhost:8000/api/items/')
                tasks.append(task)
            
            results = await asyncio.gather(*tasks)
        
        # Analyze results
        successful_requests = [r for r in results if r['status'] == 200]
        response_times = [r['response_time'] for r in results]
        
        assert len(successful_requests) >= 950  # 95% success rate
        assert statistics.mean(response_times) < 1.0  # Average < 1 second
