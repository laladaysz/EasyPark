from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from base.models import owner
from .serializers import ownerSerializer


# @api_view(['POST'])
# def receive_crop(request):
#     serializer = crop_spacesSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.erros, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_owner(request):
    owners = owner.objects.all()
    serializer = ownerSerializer(owners, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def receive_status(request):
    global parking_status
    if not isinstance(request.data, list) or not all(isinstance(d, dict) and 'spot_id' in d and 'status' in d for d in request.data):
        return Response({'error': 'Invalid data format'}, status=status.HTTP_400_BAD_REQUEST)
    
    parking_status = request.data
    return Response(request.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_status(request):
    return Response(parking_status, status=status.HTTP_200_OK)

