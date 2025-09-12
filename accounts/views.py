from rest_framework import generics, permissions
from .models import *
from .serializers import UserSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.authentication import TokenAuthentication
# views.py
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        # First, create the user using the parent class logic
        response = super().create(request, *args, **kwargs)
        
        # If user was created successfully, generate tokens
        if response.status_code == status.HTTP_201_CREATED:
            user = User.objects.get(username=request.data['username'])
            refresh = RefreshToken.for_user(user)
            
            # Add tokens to the response data
            response.data['access'] = str(refresh.access_token)
            response.data['refresh'] = str(refresh)
        
        return response
class UserDetailView(generics.RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate    

'''
#from django.contrib.auth import login as django_login  # Optional for session auth
class LoginView(APIView):
    permission_classes = ()  
    
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        
        if not username or not password:
            return Response(
                {"error": "Please provide both username and password"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(username=username, password=password)
        
        if user:
            # Get or create token for the user
            token, created = Token.objects.get_or_create(user=user)
            
            # Optional: Create session for browser-based auth
            #django_login(request, user)
            
            return Response({
                "token": token.key,
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role
            })
        else:
            return Response(
                {"error": "Wrong Credentials"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
from rest_framework.permissions import IsAuthenticated

class LogoutView(APIView):

    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Delete the token to logout
        request.user.auth_token.delete()
        return Response({"message": "Successfully logged out"})'''
    
from django.contrib.auth import logout   
class UserDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        password = request.data.get('password')
        
        if not password:
            return Response(
                {"error": "Password confirmation required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verify password
        if not request.user.check_password(password):
            return Response(
                {"error": "Invalid password"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = request.user
        
        # Optional: Add any additional cleanup here
        self._cleanup_user_data(user)
        
        # Logout before deletion
        logout(request)
        
        # Delete the user (this will trigger CASCADE deletions)
        user.delete()
        
        return Response(
            {"message": "Account and all associated data successfully deleted"},
            status=status.HTTP_204_NO_CONTENT
        )
    
    def _cleanup_user_data(self, user):
        """
        Perform additional cleanup before user deletion
        """
        # 1. Delete or handle uploaded styles
        # Since uploader has on_delete=CASCADE, styles will auto-delete
        
        # 2. Handle styles where user is credited as tailor
        from styles.models import Style
        styles_as_tailor = Style.objects.filter(tailor_user=user)
        styles_as_tailor.update(tailor_user=None)  # Set to NULL instead of deleting
        
        # 3. Clean up any other user-related data
        # Example: if you have boards, comments, likes, etc.
        # user.uploaded_boards.all().delete()  # If you have boards app
        
        # 4. Clean up social auth if you're using it
        # social_accounts = user.socialaccount_set.all()
        # social_accounts.delete()
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
        
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def change_password(request):
    new_password = request.data.get('new_password')
    confirm_password = request.data.get('confirm_password')
    
    if not new_password or not confirm_password:
        return Response(
            {"error": "Both new password and confirmation are required"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if new_password != confirm_password:
        return Response(
            {"error": "Passwords do not match"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if len(new_password) < 8:
        return Response(
            {"error": "Password must be at least 8 characters"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    request.user.set_password(new_password)
    request.user.save()
    
    return Response({"message": "Password updated successfully"})