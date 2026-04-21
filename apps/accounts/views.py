from .serializers import UserAdminSerializer, UserListSerializer, UpdatePasswordSerializer
from .models import User
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import Group
from .permissions import IsSuperUser
from drf_spectacular.utils import extend_schema

class UserAdminViewSet(viewsets.ModelViewSet):
    #serializer_class = UserAdminSerializer
    queryset = User.objects.all()
    permission_classes = [IsSuperUser]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return UserListSerializer
        elif self.action == 'change_password':
            return UpdatePasswordSerializer
        elif self.action in ['promote', 'demote']:
            return None
        return UserAdminSerializer
    
    @action(detail=True, methods=['patch'])
    def change_password(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(user, serializer.validated_data)

        return Response({'detail': 'Updated Password'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def promote(self, request, pk=None):
        user = self.get_object()
        user.is_superuser = True
        user.is_staff = True
        user.save()

        receptionis_group = Group.objects.get(name='Receptionist')
        user.groups.remove(receptionis_group)

        return Response({'detail':'promoted to superuser'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    #@extend_schema(request=None, responses={200:None})
    def demote(self, request, pk=None):
        user = self.get_object()
        user.is_superuser = False
        user.is_staff = False
        user.save()

        receptionis_group = Group.objects.get(name='Receptionist')
        user.groups.add(receptionis_group)

        return Response({'detail':'Demoted to Receptionist'})
