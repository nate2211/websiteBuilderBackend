from django.contrib.auth import authenticate
from rest_framework import generics, status, viewsets
from .models import Account, AccountImage
from .serializers import AccountSerializer, AccountRegistrationSerializer, AccountImageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

from .permissions import IsOwner, IsImageOwner
from .serializers import AccountImageSerializer
from rest_framework.parsers import MultiPartParser, FormParser


class AccountImageViewSet(viewsets.ModelViewSet):
    queryset = AccountImage.objects.all()
    serializer_class = AccountImageSerializer
    permission_classes = [IsAuthenticated, IsImageOwner]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        print(request.data)
        print(request.FILES)
        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        # Filters the queryset to include only images belonging to the requesting user's account
        return AccountImage.objects.filter(account=self.request.user)

    def perform_create(self, serializer):
        # Automatically associate the created image with the requesting user's account
        serializer.save(account=self.request.user)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        # Lists all images belonging to the requesting user's account
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        # Retrieves a specific image, ensuring it belongs to the requesting user's account
        return super().retrieve(request, *args, **kwargs)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')  # Changed from 'username' to 'email'
        password = request.data.get('password')
        user = authenticate(request, username=email,
                            password=password)  # Note: 'username=email' because authenticate expects a 'username' keyword, but we are using the email as the username.

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_id': user.id,  # Optionally return user identification
            })
        else:
            return Response({"error": "Invalid username or password."}, status=status.HTTP_401_UNAUTHORIZED)


class AccountCreateView(generics.CreateAPIView):
    serializer_class = AccountRegistrationSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Account.objects.none()

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        username = request.data.get('username')
        if Account.objects.filter(email=email).exists():
            return Response({"error": "A user with that email already exists."}, status=status.HTTP_400_BAD_REQUEST)
        if Account.objects.filter(username=username).exists():
            return Response({"error": "A user with that username already exists."}, status=status.HTTP_400_BAD_REQUEST)
        return super().post(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.id,  # Optionally return user identification
        }, status=status.HTTP_201_CREATED)


class AccountUpdateView(generics.UpdateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated, IsOwner]  # Assuming IsOwner checks if the user owns the account

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        email = request.data.get('email')
        username = request.data.get('username')
        firstname = request.data.get('firstname', None)  # Default to None if not provided
        lastname = request.data.get('lastname', None)  # Default to None if not provided
        description = request.data.get('description', None)  # Default to None if not provided
        about = request.data.get('about', None)  # Default to None if not provided

        # Check if the email or username already exists in another account
        if email and Account.objects.exclude(pk=instance.pk).filter(email=email).exists():
            return Response({"error": "A user with that email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        if username and Account.objects.exclude(pk=instance.pk).filter(username=username).exists():
            return Response({"error": "A user with that username already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Optional: Update firstname and lastname if provided
        if firstname is not None:
            instance.firstname = firstname
        if lastname is not None:
            instance.lastname = lastname

        # Optional: Update description and about if provided
        if description is not None:
            instance.description = description
        if about is not None:
            instance.about = about

        instance.save()

        # If no conflicts and optional fields are updated, proceed with the rest of the update process
        serializer = self.get_serializer(instance, data=request.data, partial=True)  # Ensure partial update
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class AccountListView(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    lookup_field = 'pk'
