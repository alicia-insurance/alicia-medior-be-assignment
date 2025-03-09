import logging
from django.shortcuts import get_object_or_404
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from url_shortener.serializers.stats_serializer import StatsSerializer
from url_shortener.models import User

logger = logging.getLogger(__name__)


class UsersView(APIView):
    throttle_classes = [AnonRateThrottle]

    def get(self, request, pk):
        url_obj = get_object_or_404(User, id=pk)
        serializer = UserSerializer(url_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
