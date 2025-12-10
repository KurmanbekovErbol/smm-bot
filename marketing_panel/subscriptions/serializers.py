from rest_framework import serializers
from .models import UserAccess

class UserAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccess
        fields = "__all__"
