from django.http import Http404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
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
    try:
        url = ShortURL.objects.get(short_code=short_code)
        url.access_count += 1
        url.save()
        return redirect(url.original_url)
    except ShortURL.DoesNotExist:
        raise Http404("No ShortURL matches the given query.")

@api_view(['GET'])
def short_url_stats(request, short_code):
    try:
        url = ShortURL.objects.get(short_code=short_code)
        return Response({
            "short_code": url.short_code,
            "original_url": url.original_url,
            "created_at": url.created_at,
            "access_count": url.access_count,
        })
    except ShortURL.DoesNotExist:
        return Response({"error": "Short URL not found"}, status=404)
