from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from base.models import crop_spaces
from .serializers import crop_spacesSerializer


@api_view(['POST'])
def receive_crop(request):
    serializer = crop_spacesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.erros, status=status.HTTP_400_BAD_REQUEST)

