from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from base.models import owner
from .serializers import ownerSerializer, PlateSpotSerializer

parking_status = []
spot_plate = []

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

@api_view(['DELETE'])
def delete_status(request):
    global parking_status
    spot_id = request.data.get('spot_id')

    updated_status = [status for status in parking_status if status['spot_id'] != spot_id]
    
    if len(updated_status) == len(parking_status):
        return Response({'error': 'spot_id not found'}, status=status.HTTP_404_NOT_FOUND)
    
    parking_status = updated_status
    return Response({'message': f'Status for spot_id {spot_id} deleted'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def receive_plate(request):
    global spot_plate  # Declara a variável global para modificá-la

    # Verifica se os dados são um dicionário e contém as chaves 'spot_id' e 'plate'
    if not isinstance(request.data, dict) or 'spot_id' not in request.data or 'plate' not in request.data:
        return Response({'error': 'Invalid data format'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Cria uma instância do serializer com os dados recebidos
    serializer = PlateSpotSerializer(data=request.data)
    
    # Verifica se os dados são válidos
    if serializer.is_valid():
        # Adiciona os dados recebidos à variável global
        spot_plate.append(serializer.validated_data)
        
        # Exemplo de resposta
        return Response({'spot_id': serializer.validated_data['spot_id'], 'plate': serializer.validated_data['plate']}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_plate(request):
    return Response(spot_plate, status=status.HTTP_200_OK)

@api_view(['POST'])
def receive_owner(request):
    serializer = ownerSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()  # Salva a nova instância do modelo Owner
        return Response(serializer.data, status=status.HTTP_201_CREATED)