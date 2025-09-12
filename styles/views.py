from rest_framework import generics, permissions
from .models import Style
from .serializers import StyleSerializer

class StyleListCreateView(generics.ListCreateAPIView):
    queryset = Style.objects.all().order_by('-created_at')
    serializer_class = StyleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(uploader=self.request.user)

class StyleDetailView(generics.RetrieveAPIView):
    queryset = Style.objects.all()
    serializer_class = StyleSerializer
    permission_classes = [permissions.AllowAny]
