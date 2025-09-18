from rest_framework import serializers
from .models import Style

class StyleSerializer(serializers.ModelSerializer):
    uploader = serializers.CharField(source='uploader.username', read_only=True)
    tailor_username = serializers.CharField(source="tailor_user.username", read_only=True)
    

    class Meta:
        model = Style
        fields = "__all__"
        read_only_fields = ('uploader','slug', 'created_at', 'updated_at') 
