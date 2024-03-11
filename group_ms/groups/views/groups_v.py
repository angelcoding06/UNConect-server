from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from groups import serializers
from rest_framework import status
from groups.views.persons_v import getPerson

# Importaciones
from groups.models import Groups,Persons
from groups.serializers.groups_s import  GroupsSerielizer

#CRUD
@api_view(['GET'])
def getGroup(request):
    group = Groups.objects.all()
    serializer = GroupsSerielizer(group, many=True)
    return Response(serializer.data)



@api_view(['POST'])
def postGroup(request):
    data = request.data
    try:
        owner_id = data.get('owner_id')
        owner_person = Persons.objects.get(id=owner_id)
    except Persons.DoesNotExist:
        return Response({'error': f'Person with ID {owner_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        group = Groups.objects.create(
            name=data['name'],
            description=data['description'],
            owner_id=owner_person,  
            is_private=data['is_private']  
        )
        members = data.get('members', [])
        admins = data.get('admins', [])
        in_requests = data.get('in_requests',[])

        for in_requests_id in in_requests:
            try:
                in_requests_person = Persons.objects.get(id=in_requests_id)
                group.in_requests.add(in_requests_person)
            except Persons.DoesNotExist:
                return Response({'error': f'Request person with ID {in_requests_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        for member_id in members:
            try:
                member_person = Persons.objects.get(id=member_id)
                group.members.add(member_person)
            except Persons.DoesNotExist:
                return Response({'error': f'Member with ID {member_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        
        for admin_id in admins:
            try:
                admin_person = Persons.objects.get(id=admin_id)
                group.admins.add(admin_person)
            except Persons.DoesNotExist:
                return Response({'error': f'Admin with ID {admin_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = GroupsSerielizer(group)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except KeyError as e:
        return Response({'error': f'Missing required field: {e}'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['DELETE'])
def deleteGroup(request, pk):
    try:
        group = Groups.objects.get(id=pk)
    except Groups.DoesNotExist:
        return Response({'error': f'Group with ID {pk} does not exist'}, status=status.HTTP_404_NOT_FOUND)
    group.delete()
    return Response({'message': f'Group with ID {pk} has been deleted'}, status=status.HTTP_204_NO_CONTENT)



@api_view(['PUT'])
def putGroup(request, pk):
    try:
        group = Groups.objects.get(id=pk)
    except Groups.DoesNotExist:
        return Response({'error': f'Group with ID {pk} does not exist'}, status=status.HTTP_404_NOT_FOUND)

    data = request.data

    if 'name' in data:
        group.name = data['name']
    if 'description' in data:
        group.description = data['description']
    if 'owner_id' in data:
        try:
            owner_person = Persons.objects.get(id=data['owner_id'])
            group.owner_id = owner_person
        except Persons.DoesNotExist:
            return Response({'error': f'Person with ID {data["owner_id"]} does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    if 'is_private' in data:
        group.is_private = data['is_private']

    try:
        group.save()
        serializer = GroupsSerielizer(group)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Metodos en constante uso
#Agregar/eliminar solicitudes
@api_view(['POST'])
def add_in_request(request, pk):
    try:
        group = Groups.objects.get(id=pk)
    except Groups.DoesNotExist:
        return Response({'error': f'Group with ID {pk} does not exist'}, status=status.HTTP_404_NOT_FOUND)

    data = request.data

    in_request_id = data.get('in_request', None)
    if in_request_id is None:
        return Response({'error': 'requester ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        in_request_person = Persons.objects.get(id=in_request_id)
    except Persons.DoesNotExist:
        return Response({'error': f'Person with ID {in_request_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    # Verificar si el grupo es privado y si el miembro está en la lista de solicitudes
    if not group.is_private:
        return Response({'error': 'Group is not private'}, status=status.HTTP_400_BAD_REQUEST)
        

    if in_request_person in group.members.all():
        return Response({'error': 'Member is already in the group'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        group.in_requests.add(in_request_person)
        serializer = GroupsSerielizer(group)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['DELETE'])
def delete_in_request(request, group_id, in_request_id):
    try:
        group = Groups.objects.get(id=group_id)
    except Groups.DoesNotExist:
        return Response({'error': f'Group with ID {group_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)

    try:
        in_request_person = Persons.objects.get(id=in_request_id)
    except Persons.DoesNotExist:
        return Response({'error': f'Person with ID {in_request_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        group.in_requests.remove(in_request_person)
        serializer = GroupsSerielizer(group)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




#Agregar/eliminar Miembro
@api_view(['POST'])
def add_member(request, pk):
    try:
        group = Groups.objects.get(id=pk)
    except Groups.DoesNotExist:
        return Response({'error': f'Group with ID {pk} does not exist'}, status=status.HTTP_404_NOT_FOUND)

    data = request.data

    member_id = data.get('member', None)
    if member_id is None:
        return Response({'error': 'Member ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        member_person = Persons.objects.get(id=member_id)
    except Persons.DoesNotExist:
        return Response({'error': f'Person with ID {member_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    # Verificar si el grupo es privado y si el miembro está en la lista de solicitudes
    if group.is_private:
        if member_person not in group.in_requests.all():
            return Response({'error': 'Member is not in the request list for this private group'}, status=status.HTTP_400_BAD_REQUEST)
        group.in_requests.remove(member_person)  # Eliminar al miembro de la lista de solicitudes

    if member_person in group.members.all():
        return Response({'error': 'Member is already in the group'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        group.members.add(member_person)
        serializer = GroupsSerielizer(group)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['DELETE'])
def delete_member(request, group_id, member_id):
    try:
        group = Groups.objects.get(id=group_id)
    except Groups.DoesNotExist:
        return Response({'error': f'Group with ID {group_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)

    try:
        member_person = Persons.objects.get(id=member_id)
    except Persons.DoesNotExist:
        return Response({'error': f'Person with ID {member_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    # Verificar si el miembro está en el grupo
    if member_person not in group.members.all():
        return Response({'error': 'Member is not in the group'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        group.members.remove(member_person)
        serializer = GroupsSerielizer(group)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#Agregar/eliminar Admin
@api_view(['POST'])
def add_admin(request, pk):
    try:
        group = Groups.objects.get(id=pk)
    except Groups.DoesNotExist:
        return Response({'error': f'Group with ID {pk} does not exist'}, status=status.HTTP_404_NOT_FOUND)

    data = request.data

    admin_id = data.get('admin', None)
    if admin_id is None:
        return Response({'error': 'Admin ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        admin_person = Persons.objects.get(id=admin_id)
    except Persons.DoesNotExist:
        return Response({'error': f'Person with ID {admin_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    # Verificar si el grupo es privado y si el miembro está en la lista de solicitudes
    if admin_person not in group.members.all():
        return Response({'error': 'Admin is not in the member list for this private group'}, status=status.HTTP_400_BAD_REQUEST)
    group.members.remove(admin_person)  # Eliminar al miembro de la lista de solicitudes

    if admin_person in group.admins.all():
        return Response({'error': 'Member is already in Admins'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        group.admins.add(admin_person)
        serializer = GroupsSerielizer(group)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['DELETE'])
def delete_admin(request, group_id, admin_id):
    try:
        group = Groups.objects.get(id=group_id)
    except Groups.DoesNotExist:
        return Response({'error': f'Group with ID {group_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)

    try:
        admin_person = Persons.objects.get(id=admin_id)
    except Persons.DoesNotExist:
        return Response({'error': f'Person with ID {admin_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    # Verificar si el miembro está en el grupo
    if admin_person not in group.admins.all():
        return Response({'error': 'Admin is not in the group'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        group.members.add(admin_person)
        group.admins.remove(admin_person)
        serializer = GroupsSerielizer(group)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)