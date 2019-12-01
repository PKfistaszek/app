from rest_framework import serializers

from .models import AppAuthor, AppPackage


class AppAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppAuthor
        fields = "__all__"


class AppPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppPackage
        fields = "__all__"
