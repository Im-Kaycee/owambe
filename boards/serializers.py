# boards/serializers.py
from rest_framework import serializers
from .models import Board
from styles.serializers import StyleSerializer  

class BoardSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    style_count = serializers.SerializerMethodField()
    class Meta:
        model = Board
        fields = '__all__'
        read_only_fields = ('owner','slug', 'created_at', 'updated_at')
    def get_style_count(self, obj):
        return obj.styles.count()
    
    def validate(self, attrs):
        # Ensure the owner can't be changed via API
        if 'owner' in attrs:
            raise serializers.ValidationError("Cannot change board owner")
        return attrs
class BoardStyleSerializer(serializers.Serializer):
    style_slug = serializers.SlugField()

class BoardWithStylesSerializer(serializers.ModelSerializer):
    styles = StyleSerializer(many=True, read_only=True)
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    
    class Meta:
        model = Board
        fields = '__all__'