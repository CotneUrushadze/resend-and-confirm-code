from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from users.serializers import UserSerializer, RegisterSerializar, PasswordResetSerializer, PasswordResetConfirmSerializer, EmailCodeResendSerializer, EmailCodeConfirmSerializer
from users.models import User, EmailVerificationCode
from rest_framework import status, serializers, mixins, viewsets, permissions, response
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import random
from django.utils import timezone
from rest_framework.decorators import action
from datetime import timedelta

class UserViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
  
    
    
class RegisterViewSet(CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializar
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            self.send_verification_code(user)
            return response.Response({'detail': 'User registered successfully and verification code sent to email'}, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def send_verification_code(self, user):
        code = str(random.randint(100000, 999999))
        
        EmailVerificationCode.objects.update_or_create(
            user=user,
            defaults={'code':code, 'created_at': timezone.now()}
        )
        subject = 'your verification code'
        massage = f"Hello {user.username}, your verification code is {code}"
        send_mail(subject, massage, 'no-reply@example.com', [user.email])
        
    @action(detail=False, methods=['post'], url_path='resend_code', serializer_class=EmailCodeResendSerializer)
    def resend_code(self, request):
        serializer = self.serializer_class(data= request.data)
        if not serializer.is_valid():
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.validated_data['user']
        existing_code = EmailVerificationCode.objects.filter(user=user).first()
        if existing_code:
            time_diff = timezone.now() - existing_code.created_at
            if time_diff < timedelta(minutes=1):
                wait_seconds = 60 - int(time_diff.total_seconds())
                return response.Response({'detail': f'დაელოდე {wait_seconds} წამი კოდის ხელახლა გასაგზავნად'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        self.send_verification_code(user)
        return response.Response({'massage': 'ვერიფიკაციის კოდი თავიდან არის გაგზავნილი'})


    @action(detail=False, methods=['post'], url_path='confirm_code', serializer_class=EmailCodeConfirmSerializer)
    def confirm_code(self, request):
        serializer = self.serializer_class(data= request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            user.is_active = True
            user.save()
            return response.Response({'massage': 'მომხმარებელი წარმატებით არის გააქტიურებული'}, status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        



class ResetPasswordViewSet(GenericViewSet, CreateModelMixin,):
    serializer_class = PasswordResetSerializer
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            reset_url = request.build_absolute_uri(
                reverse( 'password-reset-confirm', kwargs={'uidb64': uid, 'token': token},)
            )
            
            
            send_mail(
                'პაროლის აღდგენა',
                f'დააჭირეთ ლინკს რათა აღადგინოთ პაროლი {reset_url}',
                'noreply@example.com',
                [user.email],
                fail_silently=False,
            )
            
            return response.Response({'Massage': 'წერილი წარმატებით არის გაგზავნილი'}, status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        
     
class ResetPasswordConfirmViewSet(GenericViewSet, CreateModelMixin):
    serializer_class = PasswordResetConfirmSerializer       
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('uid64', openapi.IN_PATH, description='User ID (base64 encoded)', type=openapi.TYPE_STRING),
            openapi.Parameter('token', openapi.IN_PATH, description='Password reset token', type=openapi.TYPE_STRING),
        ]
    )
    
    def create(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response({'message': 'პაროლი წარმატებით შეიცვალა '}, status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
