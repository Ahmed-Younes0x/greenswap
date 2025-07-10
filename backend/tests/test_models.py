"""
Unit Tests for Models
Testing all model functionality with 95%+ coverage
"""
import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from decimal import Decimal
from accounts.models import UserProfile, UserPreferences
from items.models import Item, Category, ItemImage, Review
from security.models import SecurityLog, LoginAttempt
from ai_services.models import WasteClassification, ChatSession

User = get_user_model()

class UserModelTests(TestCase):
    """Test User and UserProfile models"""
    
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'TestPass123!',
            'first_name': 'Test',
            'last_name': 'User'
        }
    
    def test_user_creation(self):
        """Test user creation with valid data"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('TestPass123!'))
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)
    
    def test_user_profile_creation(self):
        """Test automatic profile creation"""
        user = User.objects.create_user(**self.user_data)
        self.assertTrue(hasattr(user, 'profile'))
        self.assertEqual(user.profile.user, user)
        self.assertEqual(user.profile.points, 0)
        self.assertEqual(user.profile.level, 1)
    
    def test_user_preferences_creation(self):
        """Test user preferences creation"""
        user = User.objects.create_user(**self.user_data)
        preferences = UserPreferences.objects.create(
            user=user,
            language='ar',
            theme='dark',
            notifications_enabled=True
        )
        self.assertEqual(preferences.language, 'ar')
        self.assertEqual(preferences.theme, 'dark')
        self.assertTrue(preferences.notifications_enabled)
    
    def test_invalid_email(self):
        """Test user creation with invalid email"""
        self.user_data['email'] = 'invalid-email'
        with self.assertRaises(ValidationError):
            user = User(**self.user_data)
            user.full_clean()
    
    def test_duplicate_username(self):
        """Test duplicate username validation"""
        User.objects.create_user(**self.user_data)
        with self.assertRaises(Exception):
            User.objects.create_user(**self.user_data)
    
    def test_user_str_method(self):
        """Test user string representation"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), 'testuser')
    
    def test_profile_points_update(self):
        """Test profile points update"""
        user = User.objects.create_user(**self.user_data)
        user.profile.add_points(50)
        self.assertEqual(user.profile.points, 50)
        
        user.profile.add_points(100)
        self.assertEqual(user.profile.points, 150)
    
    def test_profile_level_calculation(self):
        """Test automatic level calculation"""
        user = User.objects.create_user(**self.user_data)
        user.profile.points = 1000
        user.profile.save()
        self.assertEqual(user.profile.level, 2)
        
        user.profile.points = 5000
        user.profile.save()
        self.assertEqual(user.profile.level, 3)

class ItemModelTests(TestCase):
    """Test Item and related models"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='itemowner',
            email='owner@example.com',
            password='TestPass123!'
        )
        self.category = Category.objects.create(
            name='Electronics',
            name_ar='إلكترونيات',
            description='Electronic items'
        )
        self.item_data = {
            'title': 'Test Item',
            'title_ar': 'عنصر تجريبي',
            'description': 'Test description',
            'description_ar': 'وصف تجريبي',
            'category': self.category,
            'user': self.user,
            'condition': 'good',
            'location': 'Cairo',
            'price': Decimal('100.00'),
            'is_available': True
        }
    
    def test_item_creation(self):
        """Test item creation with valid data"""
        item = Item.objects.create(**self.item_data)
        self.assertEqual(item.title, 'Test Item')
        self.assertEqual(item.category, self.category)
        self.assertEqual(item.user, self.user)
        self.assertEqual(item.price, Decimal('100.00'))
        self.assertTrue(item.is_available)
    
    def test_item_slug_generation(self):
        """Test automatic slug generation"""
        item = Item.objects.create(**self.item_data)
        self.assertIsNotNone(item.slug)
        self.assertIn('test-item', item.slug)
    
    def test_item_str_method(self):
        """Test item string representation"""
        item = Item.objects.create(**self.item_data)
        self.assertEqual(str(item), 'Test Item')
    
    def test_item_absolute_url(self):
        """Test item absolute URL"""
        item = Item.objects.create(**self.item_data)
        expected_url = f'/items/{item.slug}/'
        self.assertEqual(item.get_absolute_url(), expected_url)
    
    def test_item_image_upload(self):
        """Test item image upload"""
        item = Item.objects.create(**self.item_data)
        image = ItemImage.objects.create(
            item=item,
            image='test_image.jpg',
            alt_text='Test image'
        )
        self.assertEqual(image.item, item)
        self.assertEqual(image.alt_text, 'Test image')
    
    def test_item_review_creation(self):
        """Test item review creation"""
        item = Item.objects.create(**self.item_data)
        reviewer = User.objects.create_user(
            username='reviewer',
            email='reviewer@example.com',
            password='TestPass123!'
        )
        review = Review.objects.create(
            item=item,
            user=reviewer,
            rating=5,
            comment='Great item!'
        )
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, 'Great item!')
    
    def test_invalid_price(self):
        """Test item creation with invalid price"""
        self.item_data['price'] = Decimal('-10.00')
        with self.assertRaises(ValidationError):
            item = Item(**self.item_data)
            item.full_clean()
    
    def test_category_str_method(self):
        """Test category string representation"""
        self.assertEqual(str(self.category), 'Electronics')

class SecurityModelTests(TestCase):
    """Test Security models"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='securitytest',
            email='security@example.com',
            password='TestPass123!'
        )
    
    def test_security_log_creation(self):
        """Test security log creation"""
        log = SecurityLog.objects.create(
            user=self.user,
            action='login',
            ip_address='192.168.1.1',
            user_agent='Test Browser',
            success=True
        )
        self.assertEqual(log.action, 'login')
        self.assertEqual(log.ip_address, '192.168.1.1')
        self.assertTrue(log.success)
    
    def test_login_attempt_tracking(self):
        """Test login attempt tracking"""
        attempt = LoginAttempt.objects.create(
            ip_address='192.168.1.1',
            username='testuser',
            success=False
        )
        self.assertEqual(attempt.username, 'testuser')
        self.assertFalse(attempt.success)

class AIModelTests(TestCase):
    """Test AI service models"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='aitest',
            email='ai@example.com',
            password='TestPass123!'
        )
    
    def test_waste_classification_creation(self):
        """Test waste classification creation"""
        classification = WasteClassification.objects.create(
            user=self.user,
            image_url='http://example.com/image.jpg',
            predicted_category='plastic',
            confidence_score=0.95,
            processing_time=1.5
        )
        self.assertEqual(classification.predicted_category, 'plastic')
        self.assertEqual(classification.confidence_score, 0.95)
    
    def test_chat_session_creation(self):
        """Test chat session creation"""
        session = ChatSession.objects.create(
            user=self.user,
            session_id='test-session-123'
        )
        self.assertEqual(session.session_id, 'test-session-123')
        self.assertTrue(session.is_active)

@pytest.mark.django_db
class ModelPerformanceTests:
    """Performance tests for models"""
    
    def test_bulk_user_creation(self):
        """Test bulk user creation performance"""
        import time
        start_time = time.time()
        
        users = []
        for i in range(100):
            users.append(User(
                username=f'user{i}',
                email=f'user{i}@example.com'
            ))
        
        User.objects.bulk_create(users)
        end_time = time.time()
        
        assert end_time - start_time < 1.0  # Should complete in under 1 second
        assert User.objects.count() == 100
    
    def test_item_query_performance(self):
        """Test item query performance"""
        # Create test data
        user = User.objects.create_user(
            username='perftest',
            email='perf@example.com',
            password='TestPass123!'
        )
        category = Category.objects.create(name='Test Category')
        
        items = []
        for i in range(50):
            items.append(Item(
                title=f'Item {i}',
                category=category,
                user=user,
                condition='good',
                location='Cairo',
                price=Decimal('100.00')
            ))
        
        Item.objects.bulk_create(items)
        
        # Test query performance
        import time
        start_time = time.time()
        
        items = Item.objects.select_related('category', 'user').all()
        list(items)  # Force evaluation
        
        end_time = time.time()
        assert end_time - start_time < 0.1  # Should complete in under 0.1 seconds
