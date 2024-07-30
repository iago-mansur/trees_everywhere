"""
Serializers for recipe APIs
"""
from rest_framework import serializers

from core.models import Tree


class TreeSerializer(serializers.ModelSerializer):
    """Serializer for trees."""

    class Meta:
        model = Tree
        fields = ['id', 'description', 'latitude', 'longitude']
        read_only_fields = ['id']


class TreeDetailSerializer(TreeSerializer):
    """Serializer for tree detail view."""

    class Meta(TreeSerializer.Meta):
        fields = TreeSerializer.Meta.fields + ['description']