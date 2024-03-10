from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from groups import serializers

# Importaciones
from groups.models import Persons
from groups.serializers.persons_s import PersonsSerielizer

@api_view(['GET'])
def getPerson(request):
    person = Persons.objects.all()
    serializer = PersonsSerielizer(person, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def postPerson(request):
    data = request.data
    person = Persons.objects.create(
        user_id = data['user_id']
    )
    serializer = PersonsSerielizer(person, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
def putPerson(request, pk):
    data = request.data
    person = Persons.objects.get(id=pk)
    serializer = PersonsSerielizer(instance=person, data=data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def deletePerson(request, pk):
    person = Persons.objects.get(id=pk)
    person.delete()
    return Response('Persona Eliminada')

