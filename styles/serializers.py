from rest_framework import serializers
from .models import Style

# serializers.py - Make sure the serializer handles partial updates
class StyleSerializer(serializers.ModelSerializer):
    uploader = serializers.CharField(source='uploader.username', read_only=True)
    tailor_username = serializers.CharField(source="tailor_user.username", read_only=True)
    
    class Meta:
        model = Style
        fields = "__all__"
        read_only_fields = ('uploader', 'slug', 'created_at', 'updated_at')
    
    def update(self, instance, validated_data):
        # Handle tailor_username separately since it's not a direct field
        tailor_username = self.context['request'].data.get('tailor_username')
        
        if tailor_username is not None:
            try:
                from accounts.models import User
                tailor_user = User.objects.get(username=tailor_username)
                instance.tailor_user = tailor_user
            except User.DoesNotExist:
                instance.tailor_user = None
        
        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance