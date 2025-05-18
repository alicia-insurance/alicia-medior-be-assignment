from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import ShortURL
from .serializers import ShortURLSerializer
from django.shortcuts import redirect, get_object_or_404

class ShortURLCreateAPIView(generics.CreateAPIView):
    queryset = ShortURL.objects.all()
    serializer_class = ShortURLSerializer

    def create(self, request, *args, **kwargs):
        original_url = request.data.get('original_url')
        obj, created = ShortURL.objects.get_or_create(original_url=original_url)
        serializer = self.get_serializer(obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

def redirect_short_url(request, short_code):
    obj = get_object_or_404(ShortURL, short_code=short_code)
    return redirect(obj.original_url)
