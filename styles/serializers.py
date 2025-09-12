from rest_framework import serializers
from .models import Style

class StyleSerializer(serializers.ModelSerializer):
    uploader_username = serializers.CharField(source="uploader.username", read_only=True)
    tailor_username = serializers.CharField(source="tailor_user.username", read_only=True)

    class Meta:
        model = Style
        fields = "__all__"
