"""
URL mappings for the tree app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from tree import views


router = DefaultRouter()
router.register('trees', views.TreeViewSet)

app_name = 'tree'

urlpatterns = [
    path('', include(router.urls)),
]