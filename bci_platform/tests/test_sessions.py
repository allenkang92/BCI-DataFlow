import pytest
from django.test import TestCase, Client
from django.urls import reverse
from bci_platform.models import Session, DataPoint
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

class SessionModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.session = Session.objects.create(
            name='Test Session',
            description='Test Description',
            created_by=self.user
        )

    def test_session_creation(self):
        """Test session creation and basic attributes"""
        self.assertEqual(self.session.name, 'Test Session')
        self.assertEqual(self.session.description, 'Test Description')
        self.assertEqual(self.session.created_by, self.user)

    def test_session_str_representation(self):
        """Test string representation of Session model"""
        self.assertEqual(str(self.session), 'Test Session')

class SessionAPITests(APITestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.session_url = reverse('session-list')

    def test_create_session(self):
        """Test creating a new session via API"""
        data = {
            'name': 'API Test Session',
            'description': 'Created via API'
        }
        response = self.client.post(self.session_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Session.objects.count(), 1)
        self.assertEqual(Session.objects.get().name, 'API Test Session')

    def test_get_sessions(self):
        """Test retrieving sessions list"""
        Session.objects.create(name='Test Session 1', created_by=self.user)
        Session.objects.create(name='Test Session 2', created_by=self.user)
        
        response = self.client.get(self.session_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

@pytest.mark.django_db
class TestSessionIntegration:
    def test_session_with_datapoints(self, client):
        """Test session creation with data points"""
        user = User.objects.create_user(username='testuser', password='12345')
        session = Session.objects.create(
            name='Integration Test Session',
            description='Testing with data points',
            created_by=user
        )
        
        # Add test data points
        DataPoint.objects.create(
            session=session,
            channel_data={'ch1': 1.0, 'ch2': 2.0},
            timestamp='2023-01-01T00:00:00Z'
        )
        
        assert session.datapoint_set.count() == 1
        assert session.datapoint_set.first().channel_data['ch1'] == 1.0
