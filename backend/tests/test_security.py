"""
Security Testing
Testing security vulnerabilities and protections
"""
import pytest
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
import json
import time
from unittest.mock import patch

User = get_user_model()

class AuthenticationSecurityTests(APITestCase):
    """Test authentication security measures"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='securitytest',
            email='security@example.com',
            password='SecurePass123!'
        )
        self.token = Token.objects.create(user=self.user)
    
    def test_password_strength_validation(self):
        """Test password strength requirements"""
        weak_passwords = [
            '123456',
            'password',
            'qwerty',
            'abc123',
            '12345678',
            'password123'
        ]
        
        for weak_password in weak_passwords:
            response = self.client.post('/api/accounts/register/', {
                'username': 'testuser',
                'email': 'test@example.com',
                'password': weak_password,
                'password_confirm': weak_password,
                'first_name': 'Test',
                'last_name': 'User'
            })
            
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn('password', response.data)
    
    def test_brute_force_protection(self):
        """Test brute force attack protection"""
        # Attempt multiple failed logins
        for i in range(6):  # Assuming 5 attempts limit
            response = self.client.post('/api/accounts/login/', {
                'username': 'securitytest',
                'password': 'wrongpassword'
            })
            
            if i < 5:
                self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            else:
                # Should be rate limited after 5 attempts
                self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
    
    def test_token_expiration(self):
        """Test token expiration"""
        # Mock expired token
        with patch('rest_framework.authtoken.models.Token.objects.get') as mock_get:
            mock_token = Token(key='expired_token', user=self.user)
            mock_token.created = time.time() - 86400  # 24 hours ago
            mock_get.return_value = mock_token
            
            self.client.credentials(HTTP_AUTHORIZATION='Token expired_token')
            response = self.client.get('/api/accounts/profile/')
            
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_session_fixation_protection(self):
        """Test session fixation protection"""
        # Get initial session
        response = self.client.get('/')
        initial_session = self.client.session.session_key
        
        # Login
        self.client.post('/api/accounts/login/', {
            'username': 'securitytest',
            'password': 'SecurePass123!'
        })
        
        # Session should change after login
        new_session = self.client.session.session_key
        self.assertNotEqual(initial_session, new_session)
    
    def test_csrf_protection(self):
        """Test CSRF protection"""
        # Attempt POST without CSRF token
        client = Client(enforce_csrf_checks=True)
        response = client.post('/api/accounts/login/', {
            'username': 'securitytest',
            'password': 'SecurePass123!'
        })
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InputValidationSecurityTests(APITestCase):
    """Test input validation security"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='inputtest',
            email='input@example.com',
            password='TestPass123!'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
    
    def test_sql_injection_protection(self):
        """Test SQL injection protection"""
        malicious_inputs = [
            "'; DROP TABLE auth_user; --",
            "' OR '1'='1",
            "'; DELETE FROM items_item; --",
            "' UNION SELECT * FROM auth_user --"
        ]
        
        for malicious_input in malicious_inputs:
            response = self.client.get(f'/api/items/?search={malicious_input}')
            
            # Should not cause server error
            self.assertNotEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # Should return normal response
            self.assertIn(response.status_code, [200, 400])
    
    def test_xss_protection(self):
        """Test XSS protection"""
        xss_payloads = [
            '<script>alert("XSS")</script>',
            '<img src="x" onerror="alert(1)">',
            'javascript:alert("XSS")',
            '<svg onload="alert(1)">',
            '"><script>alert("XSS")</script>'
        ]
        
        for payload in xss_payloads:
            response = self.client.post('/api/items/', {
                'title': payload,
                'description': 'Test description',
                'category': 1,
                'condition': 'good',
                'location': 'Cairo',
                'price': '100.00'
            })
            
            if response.status_code == 201:
                # Check that payload is escaped in response
                self.assertNotIn('<script>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        </script>',
            'email': 'test@example.com',
            'password': 'TestPass123!',
            'password_confirm': 'TestPass123!',
            'first_name': 'Test',
            'last_name': 'User'
        })
        
        if response.status_code == 201:
            assert '<script>' not in str(response.data)
        
        # 3. Attempt brute force
        for i in range(10):
            response = client.post('/api/accounts/login/', {
                'username': 'admin',
                'password': f'password{i}'
            })
        
        # Should be rate limited
        assert response.status_code == 429
    
    def test_security_monitoring(self):
        """Test security monitoring and logging"""
        from security.models import SecurityLog
        
        client = APIClient()
        
        # Perform suspicious activity
        client.post('/api/accounts/login/', {
            'username': 'admin',
            'password': 'wrongpassword'
        })
        
        # Should create security log
        logs = SecurityLog.objects.filter(action='failed_login')
        assert logs.exists()
        
        log = logs.first()
        assert log.username == 'admin'
        assert not log.success
