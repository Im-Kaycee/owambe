from rest_framework import serializers
from .models import Board
from styles.serializers import StyleSerializer

class BoardSerializer(serializers.ModelSerializer):
    styles = StyleSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = "__all__"
