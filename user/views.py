from django.contrib.auth import update_session_auth_hash, login, logout
from django.contrib.auth.models import User, Group, Permission
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

# Create your views here.
from rest_framework import status, generics, parsers, renderers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import *
from user.serializers import *


# from user.service import DeliveryInfoService


class UserCreateView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.create(
            email=serializer.validated_data['email'],
            username=serializer.validated_data['email']
        )

        user.set_password(serializer.validated_data['password'])
        user.save()

        return Response(status=status.HTTP_201_CREATED)


class UserView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        if bool(request.user.is_anonymous):
            return Response()

        return Response(UserSerializer(request.user).data)


class SellerCreateView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SellerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.create(
            email=serializer.validated_data['email'],
            username=serializer.validated_data['password']
        )

        staff_group = self.get_staff_group()
        user.groups.add(staff_group)

        user.set_password(serializer.validated_data['password'])
        user.save()

        Seller.objects.create(
            user=user,
            name=serializer.validated_data['seller']['name'],
            address=serializer.validated_data['seller']['address']
        )

        return Response(UserSerializer(user).data)

    def get_staff_group(self):
        try:
            return Group.objects.get(name='Staff')
        except ObjectDoesNotExist:
            group = Group.objects.create(name='Staff')

        all_permissions = ('add', 'change', 'delete')
        content_types = {
            'unit': all_permissions,
            'product': all_permissions,
            'unitimage': all_permissions,
            'orderunit': all_permissions,
            'order': ('change',),
            'property': ('add', 'change'),
            'propertyvalue': ('add', 'change')
        }

        for content_type in content_types:
            for permission in content_types[content_type]:
                codename = '{}_{}'.format(permission, content_type)
                permission = Permission.objects.get(codename=codename)
                group.permissions.add(permission)

        return group


class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = PasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        user.set_password(serializer.data['password'])
        user.save()

        update_session_auth_hash(request, user)

        return Response(status=status.HTTP_200_OK)


class DeliveryInfoService:

    @staticmethod
    def delete_by_user(user):
        try:
            user.deliveryinfo.delete()
            return True
        except DeliveryInfo.DoesNotExist:
            return False


class DeliveryInfoView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        try:
            deliveryinfo = user.deliveryinfo
        except DeliveryInfo.DoesNotExist:
            return Response({})

        return Response(DeliveryInfoSerializer(deliveryinfo).data)

    def post(self, request):
        serializer = DeliveryInfoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        DeliveryInfoService.delete_by_user(request.user)

        serializer.save(user=request.user)

        return Response(status=status.HTTP_201_CREATED)


class SessionAuthView(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser
    )
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response({'detail': 'Session Login Successful!'})

    def delete(self, request):
        logout(request)
        return Response({'detail': 'Session Logout Successful!'})


session_auth_view = SessionAuthView.as_view()
