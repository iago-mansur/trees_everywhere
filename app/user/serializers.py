"""
Serializers for the user API View.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _

from rest_framework import serializers
from core.models import PrimaryAccount


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""
    primary_accounts = serializers.PrimaryKeyRelatedField(many=True,
                                                          queryset=PrimaryAccount.objects.all()
                                                          , required=False)


    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name', 'primary_accounts']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5},
            'primary_accounts': {'read_only': True}
        }

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        primary_accounts = validated_data.pop('primary_accounts', [])
        user = get_user_model().objects.create_user(**validated_data)
        user.primary_accounts.set(primary_accounts)
        return user

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None)
        primary_accounts = validated_data.pop('primary_accounts', [])

        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        if primary_accounts:
            user.primary_accounts.set(primary_accounts)


        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs