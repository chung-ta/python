import datetime

from django.shortcuts import render

# Create your views here.
from rest_framework import status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from rest_framework.permissions import  AllowAny
from rest_framework import serializers
from rest_framework_jwt.views import jwt_response_payload_handler

from user_locator_cass.api.models import Account, AdminUser
from user_locator_cass.api.permissions import IsAuthenticated
from user_locator_cass.api.serializers import AccountSerializer, AdminUserSerializer
from user_locator_cass.api.apps import us_location
from user_locator_cass.api.service import location_service


class AccountViewSet(viewsets.ViewSet):

    permission_classes = (IsAuthenticated,)
    def list(self, request):
        global us_location
        queryset = Account.objects.all()
        serializer = AccountSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Account.objects.all()
        filter = {}
        filter['username'] = pk
        account = get_object_or_404(queryset, **filter)
        serializer = AccountSerializer(account)
        return Response(serializer.data)

    def create(self, request, formant=None):
        serializer  = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLocatorViewSet(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):
        # ''' Gets k users that are closet to the specified lat/long
        #
        #     Path Parameters : username
        #
        #     Query Paramater : lat (required)
        #
        #     Query Paramater : long (requried)
        #
        #     Query Parameter : k (optional) - the number of users nearest to this lat/long.  Default value for k = 3
        #
        #     Returns : list of users that are closet to the specified lat/long
        # '''
        lat =  request.query_params['lat']
        long = request.query_params['long']
        k =  request.query_params['k']
        if not k :
             k = 3
        k_nearest_locs = location_service.find_k_closet(float(lat), float(long), int(k))
        print(k_nearest_locs)
        # print(k_nearest_locs[1])
        # user_infos = [dict(user_locations[index], **{'distance': round(distance,2)}) for distance, index in
        #              zip(k_nearest_locs[0], k_nearest_locs[1])]
        # return sorted(user_infos, key=operator.itemgetter('distance'))
        return Response({'success': 1})

class AdminTokenViewSet(APIView):

    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        serializer = AdminUserSerializer(data=request.data)

        if serializer.is_valid():
            queryset = AdminUser.objects.all()
            filter = {}
            filter['username'] = serializer.data['username']
            filter['password'] = serializer.data['password']
            admin_user = get_object_or_404(queryset, **filter)
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            payload = jwt_payload_handler(admin_user)
            token = jwt_encode_handler(payload)
            token_dic = {"token" : token}
            return Response(token_dic)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)