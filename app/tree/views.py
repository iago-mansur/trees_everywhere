"""
Views for the recipe APIs
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tree
from tree import serializers


class TreeViewSet(viewsets.ModelViewSet):
    """View for manage tree APIs."""
    serializer_class = serializers.TreeDetailSerializer
    queryset = Tree.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve trees for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.TreeSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new tree."""
        serializer.save(user=self.request.user)