"""
Tests for tree APIs.
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tree

from tree.serializers import (
    TreeSerializer,
    TreeDetailSerializer,
)


TREES_URL = reverse('tree:tree-list')


def detail_url(tree_id):
    """Create and return a tree detail URL."""
    return reverse('tree:tree-detail', args=[tree_id])


def create_tree(user, **params):
    """Create and return a sample tree."""
    defaults = {
        'description': 'Sample tree description.',
        'latitude': Decimal('11.123456'),
        'longitude': Decimal('21.123456'),
    }
    defaults.update(params)

    tree = Tree.objects.create(user=user, **defaults)
    return tree


class PublicTreeAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(TREES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTreeApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_tree(self):
        """Test retrieving a list of tree."""
        create_tree(user=self.user)
        create_tree(user=self.user)

        res = self.client.get(TREES_URL)

        trees = Tree.objects.all().order_by('-id')
        serializer = TreeSerializer(trees, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tree_list_limited_to_user(self):
        """Test list of tree is limited to authenticated user."""
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'password123',
        )
        create_tree(user=other_user)
        create_tree(user=self.user)

        res = self.client.get(TREES_URL)

        trees = Tree.objects.filter(user=self.user)
        serializer = TreeSerializer(trees, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_tree_detail(self):
        """Test get tree detail."""
        tree = create_tree(user=self.user)

        url = detail_url(tree.id)
        res = self.client.get(url)

        serializer = TreeDetailSerializer(tree)
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe(self):
        """Test creating a tree."""
        payload = {
            'description': 'Sample tree description.',
            'latitude': Decimal('12.123456'),
            'longitude': Decimal('23.123456'),
        }
        res = self.client.post(TREES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        tree = Tree.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(tree, k), v)
        self.assertEqual(tree.user, self.user)
