__author__ = 'mstacy'
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import serializers, generics
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .models import AuthtokenToken
class APIRoot(APIView):
    permission_classes = ( IsAuthenticatedOrReadOnly,)

    def get(self, request,format=None):
        # Assuming we have views named 'foo-view' and 'bar-view'
        # in our project's URLconf.
        return Response({
            'Queue': {'Tasks': reverse('queue-main', request=request),
                      'Tasks History': reverse('queue-user-tasks',request=request)},
            'Catalog': {'Data Source':reverse('source-list',request=request)},
            'Data Store': {'Mongo':reverse('data-list',request=request)},
        })



class UserSerializer(serializers.Serializer):
    #api_detail_url = serializers.HyperlinkedIdentityField(lookup_field='id', view_name='user-detail')

    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    #auth_token = serializers.reverse('token-detail')
    #def to_representation(self, obj):
    ##    obj['auth_token']= Token.objects.get_or_create(user=self.request.user)
    #    return obj

class AuthToken(APIView):
    permission_classes = ( IsAuthenticatedOrReadOnly,)
    #model = Token
    def get(self,request,id=None,format=None):
        tok = Token.objects.get_or_create(user=self.request.user)
        #print tok.key
        return Response({"User":self.request.user.username,"Auth-Token":str(tok[0])})
class UserProfile(APIView):
    permission_classes = ( IsAuthenticated,)
    serializer_class = UserSerializer
    model = User
    def get(self,request,id=None,format=None):
    #def get_queryset(self):
        data = User.objects.get(pk=self.request.user.id)
        print data
        serializer = self.serializer_class(data,context={'request':request})
        tok = Token.objects.get_or_create(user=self.request.user)
        data = serializer.data
        data['auth-token']= str(tok[0])
        #print serializer.data
        return Response(data)
    #def get(self,request,format=None):
     #   data = User.objects.all()
      #  print data
      #  return Response(data)
class UserDetail(generics.RetrieveAPIView):
    model = User
    #queryset = User.objects.all()
    serializer_class = UserSerializer
    def get_queryset(self):
        data = User.objects.get(username=self.request.user.username)
        print data
        return data


from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user