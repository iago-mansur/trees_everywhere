"""
Tests for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import PrimaryAccount

class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email = email,
            password = password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users"""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.com', 'test4@example.com'],

        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_user_primary_account_association(self):
        """Test creating a user associates it with a primary account."""
        email = 'test@example.com'
        password = 'testpass123'
        account_name = 'Primary Account'

        primary_account = PrimaryAccount.objects.create(name=account_name)
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            primary_account=primary_account
        )

        self.assertEqual(user.primary_account.name, account_name)
        self.assertEqual(primary_account.account_users.first(), user)