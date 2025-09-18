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
        serializer.save(uploader=self.request.user)

class StyleDetailView(generics.RetrieveAPIView):
    queryset = Style.objects.all()
    serializer_class = StyleSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

# Add Update and Delete views
class StyleUpdateView(generics.UpdateAPIView):
    queryset = Style.objects.all()
    serializer_class = StyleSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        # Users can only update their own styles
        return Style.objects.filter(uploader=self.request.user)

class StyleDeleteView(generics.DestroyAPIView):
    queryset = Style.objects.all()
    serializer_class = StyleSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [UserRateThrottle]

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
    