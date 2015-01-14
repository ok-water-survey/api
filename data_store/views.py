# from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from pymongo import MongoClient
from api import config
from .models import dumb_model
# Create your views here.
from rest_framework.settings import api_settings
from .mongo_paginator import MongoDataPagination
from .renderer import DataBrowsableAPIRenderer, mongoJSONPRenderer,mongoJSONRenderer
from rest_framework.renderers import XMLRenderer, YAMLRenderer,JSONPRenderer
from rest_framework.parsers import JSONParser

class MongoDataStore(APIView):
    permission_classes = ( IsAuthenticatedOrReadOnly,)
    renderer_classes = (DataBrowsableAPIRenderer, mongoJSONRenderer, mongoJSONPRenderer, XMLRenderer, YAMLRenderer)
    title = "Database"
    parser_classes = (JSONParser,)
    def __init__(self, connect_uri=config.DATA_STORE_MONGO_URI):
        self.db = MongoClient(host=connect_uri)

    def get(self, request, database=None, format=None):
        urls = []
        if database:
            self.title = "Collection"
            data = list(self.db[database].collection_names())
            #print data
            data.sort()
            for col in data:
                urls.append(reverse('data-detail', kwargs={'database': database, 'collection': col}, request=request))
            return Response({'Database': database, 'Available Collections': urls})
        else:
            self.title = "Database"
            data = list(self.db.database_names())
            data.sort()
            for db in data:
                urls.append(reverse('data-list', kwargs={'database': db}, request=request))
            return Response({
                'Available Databases': urls})


class DataStore(APIView):
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
    model = dumb_model
    renderer_classes = (DataBrowsableAPIRenderer, mongoJSONRenderer, mongoJSONPRenderer, XMLRenderer, YAMLRenderer)
    parser_classes = (JSONParser,)
    def __init__(self, connect_uri=config.DATA_STORE_MONGO_URI):
        self.db = MongoClient(host=connect_uri)

    def get(self, request, database=None, collection=None, format=None):
        query = request.QUERY_PARAMS.get('query', None)
        page_size = request.QUERY_PARAMS.get(api_settings.user_settings.get('PAGINATE_BY_PARAM', 'page_size'),
                                             api_settings.user_settings.get('PAGINATE_BY', 10))
        try:
            page = int(request.QUERY_PARAMS.get('page', 1))
        except:
            page = 1
        try:
            page_size = int(page_size)
        except:
            page_size = int(api_settings.user_settings.get('PAGINATE_BY', 10))

        url = request and request.build_absolute_uri() or ''
        data = MongoDataPagination(self.db, database, collection, query=query, page=page, nPerPage=page_size, uri=url)
        return Response(data)
    def post(self,request,database=None,collection=None,format=None):
        return Response(request.DATA)

"""
        if query:
            query = ast.literal_eval(query)
            print query
            q = [ (k, v) for k, v in query['spec'].items() ]
            query['spec'] = dict(q)
            print query
            data = [row for row in self.db[database][collection].find(**query)]
        else:
            data = [row for row in self.db[database][collection].find()]

        paginator = Paginator(data,page_size)

        try:
            result =paginator.page(page)
        except PageNotAnInteger:
            result = paginator.page(1)
        except EmptyPage:
            result = paginator.page(paginator.num_pages)
        serializer = PaginationSerializer(instance=result,context={'request': request})
        return Response(serializer.data)
    #def put(self,request,database=None,collection=None,format=None):
    #    return Response(request.DATA)

"""