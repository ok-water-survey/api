from django.shortcuts import render
from rest_framework_mongoengine import generics
from .models import Source, SourceSerializer #, SourceFilter
from rest_framework.parsers import JSONParser
from .permission import DjangoMongoPermissionsOrAnonReadOnly
# Create your views here.
class SourceList(generics.ListCreateAPIView):
    #permission_classes = (DjangoMongoPermissionsOrAnonReadOnly)
    serializer_class = SourceSerializer
    model = Source
    queryset = Source.objects.all() #(model='Source')
    parser_classes = (JSONParser,)

class SourceDetail(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = (DjangoMongoPermissionsOrAnonReadOnly)
    serializer_class = SourceSerializer
    model = Source
    parser_classes = (JSONParser,)
    #queryset = Source.objects(id=request.parser_context['kwargs']['id'])
    #filter_backend = SourceFilter
    def get_queryset(self):
        return Source.objects(id=self.request.parser_context['kwargs']['id'])