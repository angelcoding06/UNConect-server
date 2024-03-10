from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from groups import serializers

# Importaciones
from groups.models import Groups
from groups.serializers.groups_s import  GroupsSerielizer

@api_view(['GET'])
def getGroup(request):
    group = Groups.objects.all()
    serializer = GroupsSerielizer(group, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def post(request):
    data = request.data
    person = Groups.objects.create(
        user_id = data['user_id']
        name = models.CharField(max_length=200)
        description = models.TextField()
        owner_id = models.OneToOneField(Persons, on_delete=models.CASCADE)
        members = models.ManyToManyField(Persons, related_name='miembros')
        admins = models.ManyToManyField(Persons, related_name='administradores')
        is_private = models.BooleanField()
    )
    serializer = GroupsSerielizer(person, many=False)
    return Response(serializer.data)