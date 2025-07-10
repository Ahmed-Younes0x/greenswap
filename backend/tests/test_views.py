"""
Integration Tests for Views
Testing API endpoints and view functionality
"""
import json
import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from items.models import Item, Category
from accounts.models import UserProfile

User = get_user_model()

class AuthenticationViewTests(APITestCase):
    """Test authentication endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('accounts:register')
        self.login_url = reverse('accounts:login')
        self.profile_url = reverse('accounts:profile')
        
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'TestPass123!',
            'password_confirm': 'TestPass123!',
            'first_name': 'Test',
            'last_name': 'User'
        }
    
    def test_user_registration(self):
        """Test user registration endpoint"""
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertTrue(User.objects.filter(username='testuser').exists())
    
    def test_user_registration_invalid_data(self):
        """Test registration with invalid data"""
        invalid_data = self.user_data.copy()
        invalid_data['email'] = 'invalid-email'
        
        response = self.client.post(self.register_url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_registration_password_mismatch(self):
        """Test registration with password mismatch"""
        invalid_data = self.user_data.copy()
        invalid_data['password_confirm'] = 'DifferentPass123!'
        
        response = self.client.post(self.register_url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_login(self):
        """Test user login endpoint"""
        # Create user first
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!'
        )
        
        login_data = {
            'username': 'testuser',
            'password': 'TestPass123!'
        }
        
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
    
    def test_user_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        login_data = {
            'username': 'nonexistent',
            'password': 'WrongPass123!'
        }
        
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_profile_access_authenticated(self):
        """Test profile access with authentication"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!'
        )
        token = Token.objects.create(user=user)
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        response = self.client.get(self.profile_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
    
    def test_profile_access_unauthenticated(self):
        """Test profile access without authentication"""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class ItemViewTests(APITestCase):
    """Test item-related endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='itemowner',
            email='owner@example.com',
            password='TestPass123!'
        )
        self.token = Token.objects.create(user=self.user)
        self.category = Category.objects.create(
            name='Electronics',
            description='Electronic items'
        )
        
        self.item_data = {
            'title': 'Test Item',
            'description': 'Test description',
            'category': self.category.id,
            'condition': 'good',
            'location': 'Cairo',
            'price': '100.00'
        }
        
        self.items_url = reverse('items:item-list')
    
    def test_item_creation_authenticated(self):
        """Test item creation with authentication"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(self.items_url, self.item_data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Test Item')
        self.assertTrue(Item.objects.filter(title='Test Item').exists())
    
    def test_item_creation_unauthenticated(self):
        """Test item creation without authentication"""
        response = self.client.post(self.items_url, self.item_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_item_list_public(self):
        """Test public item list access"""
        # Create some test items
        Item.objects.create(
            title='Public Item',
            category=self.category,
            user=self.user,
            condition='good',
            location='Cairo',
            price=100.00
        )
        
        response = self.client.get(self.items_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
    
    def test_item_detail_view(self):
        """Test item detail view"""
        item = Item.objects.create(
            title='Detail Item',
            category=self.category,
            user=self.user,
            condition='good',
            location='Cairo',
            price=100.00
        )
        
        detail_url = reverse('items:item-detail', kwargs={'slug': item.slug})
        response = self.client.get(detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Detail Item')
    
    def test_item_search(self):
        """Test item search functionality"""
        Item.objects.create(
            title='Searchable Item',
            category=self.category,
            user=self.user,
            condition='good',
            location='Cairo',
            price=100.00
        )
        
        search_url = f"{self.items_url}?search=Searchable"
        response = self.client.get(search_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
    
    def test_item_filter_by_category(self):
        """Test item filtering by category"""
        Item.objects.create(
            title='Electronics Item',
            category=self.category,
            user=self.user,
            condition='good',
            location='Cairo',
            price=100.00
        )
        
        filter_url = f"{self.items_url}?category={self.category.id}"
        response = self.client.get(filter_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
    
    def test_item_update_owner(self):
        """Test item update by owner"""
        item = Item.objects.create(
            title='Update Item',
            category=self.category,
            user=self.user,
            condition='good',
            location='Cairo',
            price=100.00
        )
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        update_url = reverse('items:item-detail', kwargs={'slug': item.slug})
        
        update_data = {'title': 'Updated Item'}
        response = self.client.patch(update_url, update_data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Item')
    
    def test_item_delete_owner(self):
        """Test item deletion by owner"""
        item = Item.objects.create(
            title='Delete Item',
            category=self.category,
            user=self.user,
            condition='good',
            location='Cairo',
            price=100.00
        )
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        delete_url = reverse('items:item-detail', kwargs={'slug': item.slug})
        
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Item.objects.filter(id=item.id).exists())

class AIServiceViewTests(APITestCase):
    """Test AI service endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='aiuser',
            email='ai@example.com',
            password='TestPass123!'
        )
        self.token = Token.objects.create(user=self.user)
        
        self.classify_url = reverse('ai_services:classify-waste')
        self.chat_url = reverse('ai_services:chat')
    
    def test_waste_classification_authenticated(self):
        """Test waste classification with authentication"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        # Mock image data
        classification_data = {
            'image_url': 'http://example.com/waste.jpg'
        }
        
        response = self.client.post(self.classify_url, classification_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('category', response.data)
        self.assertIn('confidence', response.data)
    
    def test_waste_classification_unauthenticated(self):
        """Test waste classification without authentication"""
        classification_data = {
            'image_url': 'http://example.com/waste.jpg'
        }
        
        response = self.client.post(self.classify_url, classification_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_ai_chat_authenticated(self):
        """Test AI chat with authentication"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        chat_data = {
            'message': 'How do I recycle plastic?',
            'session_id': 'test-session-123'
        }
        
        response = self.client.post(self.chat_url, chat_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('response', response.data)
        self.assertIn('session_id', response.data)

class SecurityViewTests(APITestCase):
    """Test security-related endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='securityuser',
            email='security@example.com',
            password='TestPass123!'
        )
        self.token = Token.objects.create(user=self.user)
        
        self.security_logs_url = reverse('security:logs')
        self.change_password_url = reverse('security:change-password')
    
    def test_security_logs_access(self):
        """Test security logs access"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(self.security_logs_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
    
    def test_password_change(self):
        """Test password change functionality"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        password_data = {
            'old_password': 'TestPass123!',
            'new_password': 'NewTestPass123!',
            'new_password_confirm': 'NewTestPass123!'
        }
        
        response = self.client.post(self.change_password_url, password_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify password was changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewTestPass123!'))

@pytest.mark.django_db
class ViewPerformanceTests:
    """Performance tests for views"""
    
    def test_item_list_performance(self):
        """Test item list view performance"""
        client = APIClient()
        
        # Create test data
        user = User.objects.create_user(
            username='perfuser',
            email='perf@example.com',
            password='TestPass123!'
        )
        category = Category.objects.create(name='Test Category')
        
        items = []
        for i in range(100):
            items.append(Item(
                title=f'Item {i}',
                category=category,
                user=user,
                condition='good',
                location='Cairo',
                price=100.00
            ))
        
        Item.objects.bulk_create(items)
        
        # Test performance
        import time
        start_time = time.time()
        
        response = client.get('/api/items/')
        
        end_time = time.time()
        
        assert response.status_code == 200
        assert end_time - start_time < 1.0  # Should complete in under 1 second
        assert len(response.data['results']) > 0
