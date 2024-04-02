from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from groups import serializers
from rest_framework import status

# Importaciones
from groups.models import Persons
from groups.serializers.persons_s import PersonsSerielizer

@api_view(['GET'])
def getPerson(request):
    if request.method != 'GET':
        return Response({"error": "Método no permitido"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        person = Persons.objects.all()
        serializer = PersonsSerielizer(person, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def postPerson(request):
    try:
        data = request.data
        person = Persons.objects.create(
            user_id=data['user_id']
        )
        serializer = PersonsSerielizer(person, many=False)
        return Response(serializer.data)
    except KeyError as e:
        return Response({"error": f"Falta el campo '{e.args[0]}' en los datos proporcionados"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
def putPerson(request, pk):
    try:
        data = request.data
        person = Persons.objects.get(id=pk)
        serializer = PersonsSerielizer(instance=person, data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    except Persons.DoesNotExist:
        return Response({"error": f"No se encontró una persona con el ID '{pk}'"}, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def deletePerson(request, pk):
    try:
        person = Persons.objects.get(id=pk)
        person.delete()
        return Response({'message': f'Person with ID {pk} has been deleted'})
    except Persons.DoesNotExist:
        return Response({"error": f"No se encontró una persona con el ID '{pk}'"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)