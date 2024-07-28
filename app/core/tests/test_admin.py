"""
Tests for the Django admin modifications.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client

from core.models import PrimaryAccount


class AdminSiteTests(TestCase):
    """Tests for Django admin."""

    def setUp(self):
        """Create user and cliente."""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='testpass123',
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testpass123',
            name='Test User'
        )
        self.primary_account = PrimaryAccount.objects.create(name='Test Account')

    def test_users_list(self):
        """Test that users are listed on page."""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test the edit user page works."""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test the create user page works."""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code,200)

    def test_primary_accounts_list(self):
        """Test that primary accounts are listed on page."""
        url = reverse('admin:core_primaryaccount_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.primary_account.name)

    def test_edit_primary_account_page(self):
        """Test the edit primary account page works."""
        url = reverse('admin:core_primaryaccount_change', args=[self.primary_account.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_primary_account_page(self):
        """Test the create primary account page works."""
        url = reverse('admin:core_primaryaccount_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_edit_user_page_contains_primary_account(self):
        """Test the edit user page contains the primary account field."""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertContains(res, 'Primary account')
