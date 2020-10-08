import time

from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import serializers

from .models import (
    Auto,
    Partner,
    AutoPartnerConnection
)


@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def partner_list_create(request):
    # LIST
    if request.method == 'GET':
        partnerek = Partner.objects.filter(deleted_at=None)
        serializer = serializers.PartnerSerializer(
            partnerek,
            many=True,
            context={
                'query': request.query_params.get('query', 'flat')
            }
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    # CREATE
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = serializers.PartnerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def partner_detail_delete(request, pk):
    try:
        partner = Partner.objects.filter(deleted_at=None).get(pk=pk)
    except Partner.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # DETAIL
    if request.method == 'GET':
        serializer = serializers.PartnerSerializer(
            partner,
            context={
                'query': request.query_params.get('query', 'flat')
            }
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    # DELETE
    elif request.method == 'DELETE':
        partner.deleted_at = int(time.time())
        partner.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def auto_list_create(request):
    # LIST
    if request.method == 'GET':
        autok = Auto.objects.filter(deleted_at=None)
        serializer = serializers.AutoSerializer(
            autok,
            many=True,
            context={
                'query': request.query_params.get('query', 'flat')
            }
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    # CREATE
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = serializers.AutoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET', 'DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def auto_detail_delete(request, pk):
    try:
        auto = Auto.objects.filter(deleted_at=None).get(pk=pk)
    except Auto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # DETAIL
    if request.method == 'GET':
        serializer = serializers.AutoSerializer(
            auto,
            context={
                'query': request.query_params.get('query', 'flat')
            }
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    # DELETE
    elif request.method == 'DELETE':
        auto.deleted_at = int(time.time())
        auto.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    # CREATE
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        if data.get('partner'):
            data['auto'] = auto.id
            serializer = serializers.AutoPartnerConnectionSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# @csrf_exempt
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def autopartnerkapcsolat_list(request):
#     if request.method == 'GET':
#         kapcsolat = AutoPartnerConnection.objects.filter(deleted_at=None)
#         serializer = serializers.AutoPartnerConnectionSerializer(
#             kapcsolat,
#             many=True
#         )
#         return Response(serializer.data, status=status.HTTP_200_OK)


# @csrf_exempt
# @api_view(['GET', 'DELETE'])
# @permission_classes([IsAuthenticated])
# def autopartnerkapcsolat_detail_delete(request, pk):
#     try:
#         kapcsolat = AutoPartnerConnection.objects.filter(deleted_at=None).get(pk=pk)
#     except AutoPartnerConnection.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = serializers.AutoPartnerConnectionSerializer(kapcsolat)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == 'DELETE':
#         kapcsolat.deleted_at = int(time.time())
#         kapcsolat.save()
#         return Response(status=status.HTTP_204_NO_CONTENT)
