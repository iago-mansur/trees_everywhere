"""
Tests for the Django admin modifications.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client

from core.models import Account


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
        self.accounts = [Account.objects.create(name=f'Account {i}') for i in range(3)]
        self.user.accounts.set(self.accounts)
        self.user.refresh_from_db()

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

    def test_accounts_list(self):
        """Test that accounts are listed on page."""
        url = reverse('admin:core_account_changelist')
        res = self.client.get(url)

        for account in self.accounts:
            self.assertContains(res, account.name)

    def test_edit_account_page(self):
        """Test the edit account page works."""
        url = reverse('admin:core_account_change', args=[self.accounts[0].id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_account_page(self):
        """Test the create account page works."""
        url = reverse('admin:core_account_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_edit_user_page_contains_account(self):
        """Test the edit user page contains the accounts field."""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertContains(res, 'Accounts')
