from rest_framework import generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Style
from .serializers import StyleSerializer
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
class StyleListCreateView(generics.ListCreateAPIView):
    queryset = Style.objects.all().order_by('-created_at')
    serializer_class = StyleSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    
    def perform_create(self, serializer):
        tailor_username = self.request.data.get('tailor_username')
        tailor_user = None
        
        if tailor_username:
            try:
                from accounts.models import User
                tailor_user = User.objects.get(username=tailor_username)
            except User.DoesNotExist:
                # If tailor username doesn't exist, we'll just set the name fields
                pass
        
        serializer.save(
            uploader=self.request.user,
            tailor_user=tailor_user
        )

class StyleDetailView(generics.RetrieveAPIView):
    queryset = Style.objects.all()
    serializer_class = StyleSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

class StyleUpdateView(generics.UpdateAPIView):
    queryset = Style.objects.all()
    serializer_class = StyleSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    lookup_field = 'slug'

    def get_queryset(self):
        return Style.objects.filter(uploader=self.request.user)
    
    def perform_update(self, serializer):
        tailor_username = self.request.data.get('tailor_username')
        tailor_user = None
        
        if tailor_username:
            try:
                from accounts.models import User
                tailor_user = User.objects.get(username=tailor_username)
            except User.DoesNotExist:
                # If tailor username doesn't exist, set to None
                tailor_user = None
        
        # Save with the found tailor user or None if not found
        serializer.save(tailor_user=tailor_user)
class StyleDeleteView(generics.DestroyAPIView):
    queryset = Style.objects.all()
    serializer_class = StyleSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    lookup_field = 'slug'

    def get_queryset(self):
        # Users can only delete their own styles
        return Style.objects.filter(uploader=self.request.user)
    
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.db.models import Q

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.AllowAny])
def style_search(request):
    """
    Search styles by title, category, fabric, occasion, or color
    """
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    
    styles = Style.objects.all()
    
    if query:
        styles = styles.filter(
            Q(title__icontains=query) |
            Q(fabric_type__icontains=query) |
            Q(occasion__icontains=query) |
            Q(colour__icontains=query)
        )
    
    if category:
        styles = styles.filter(category=category)
    
    serializer = StyleSerializer(styles, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def user_styles(request):
    """
    Get all styles uploaded by the current user
    """
    styles = Style.objects.filter(uploader=request.user).order_by('-created_at')
    serializer = StyleSerializer(styles, many=True)
    return Response(serializer.data)

class StyleListView(generics.ListAPIView):
    queryset = Style.objects.all().order_by('-created_at')
    serializer_class = StyleSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.AllowAny]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    