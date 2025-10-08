from django.shortcuts import render

# Create your views here.
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer, LoginSerializer

# Registration API
class RegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]  # Anyone can register

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "message": "User registered successfully"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login API
class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]  # Anyone can login

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "message": "Login successful"
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from rest_framework import generics, permissions
from django.utils import timezone
from .models import GameMode
from .serializers import GameModeSerializer

class CreateGameModeView(generics.CreateAPIView):
    serializer_class = GameModeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        today = timezone.now().date()
        user = self.request.user

        # Count existing attempts for today for this user using 'date' field
        attempts_today = GameMode.objects.filter(
            user=user,
            date=today
        ).count()

        serializer.save(
            user=user,
            attempt=attempts_today + 1,
            date=today  # explicitly set the date field
        )

from rest_framework.response import Response
from rest_framework import status
from .models import GameQuestionRecord
from .serializers import GameQuestionRecordSerializer

class CreateGameRecordsView(generics.GenericAPIView):
    serializer_class = GameQuestionRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        records = request.data  # Expecting a list of records
        if not isinstance(records, list):
            return Response({"error": "Expected a list of records"}, status=status.HTTP_400_BAD_REQUEST)

        # Optional: ensure user can only post records for their own game_mode
        for r in records:
            if 'game_mode' not in r:
                return Response({"error": "game_mode is required for each record"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=records, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # will assign all records properly

        return Response({"status": "success", "saved": len(records)}, status=status.HTTP_201_CREATED)
    
    
    
class UpdateGameModeIQView(generics.UpdateAPIView):
    queryset = GameMode.objects.all()
    serializer_class = GameModeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        game_mode = self.get_object()

        # Only allow the owner to update
        if game_mode.user != request.user:
            return Response({"detail": "Not allowed."}, status=status.HTTP_403_FORBIDDEN)

        iq = request.data.get("iq")
        if iq is None:
            return Response({"detail": "IQ value is required."}, status=status.HTTP_400_BAD_REQUEST)

        game_mode.iq = iq
        game_mode.save()
        serializer = self.get_serializer(game_mode)
        return Response(serializer.data, status=status.HTTP_200_OK)