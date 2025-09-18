from rest_framework import generics, permissions
from .models import Board
from .serializers import BoardSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

class BoardListCreateView(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'slug'
    lookup_url_kwarg = 'board_slug' 
    
    def get_queryset(self):
        return Board.objects.filter(owner=self.request.user)
    
class BoardDeleteView(generics.DestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'slug'  # Add this line
    lookup_url_kwarg = 'board_slug'  # Add this line to match your URL parameter
    
    def get_queryset(self):
        return Board.objects.filter(owner=self.request.user)
class UserBoardsView(generics.ListAPIView):
    serializer_class = BoardSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get_queryset(self):
        return Board.objects.filter(owner=self.request.user).order_by('-created_at')
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def add_collaborator(request, board_id):
    try:
        board = Board.objects.get(id=board_id, owner=request.user)
        collaborator_username = request.data.get('username')
        
        # Get the user to add as collaborator
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        collaborator = User.objects.get(username=collaborator_username)
        board.collaborators.add(collaborator)
        board.save()
        
        return Response({"message": f"Added {collaborator_username} as collaborator"})
        
    except Board.DoesNotExist:
        return Response({"error": "Board not found or you don't own it"}, status=404)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)


from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from styles.models import Style
from .serializers import BoardStyleSerializer
from styles.serializers import StyleSerializer
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def add_style_to_board(request, board_slug):
    try:
        # Get the board (user must own it)
        board = Board.objects.get(slug=board_slug, owner=request.user)
        
        # Validate input
        serializer = BoardStyleSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Get the style
        style_slug = serializer.validated_data['style_slug']
        try:
            style = Style.objects.get(slug=style_slug)
        except Style.DoesNotExist:
            return Response(
                {"error": "Style not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Add style to board
        board.styles.add(style)
        
        return Response({
            "message": f"Added '{style.title}' to board '{board.name}'"
        })
        
    except Board.DoesNotExist:
        return Response(
            {"error": "Board not found or you don't own it"}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def remove_style_from_board(request, board_slug):
    try:
        # Get the board (user must own it)
        board = Board.objects.get(slug=board_slug, owner=request.user)
        
        # Validate input
        serializer = BoardStyleSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Get the style
        style_slug = serializer.validated_data['style_slug']
        try:
            style = Style.objects.get(slug=style_slug)
        except Style.DoesNotExist:
            return Response(
                {"error": "Style not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Remove style from board
        board.styles.remove(style)
        
        return Response({
            "message": f"Removed '{style.title}' from board '{board.name}'"
        })
        
    except Board.DoesNotExist:
        return Response(
            {"error": "Board not found or you don't own it"}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def get_board_styles(request, board_slug):
    """
    Get all styles in a board
    """
    try:
        # Get the board (user must own it, or it must be public)
        board = Board.objects.get(slug=board_slug)
        
        # Check permissions
        if board.owner != request.user:
            return Response(
                {"error": "You don't have permission to view this board"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get styles with full details
        styles = board.styles.all()
        style_serializer = StyleSerializer(styles, many=True)
        
        return Response({
            "board": board.name,
            "styles": style_serializer.data
        })
        
    except Board.DoesNotExist:
        return Response(
            {"error": "Board not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )