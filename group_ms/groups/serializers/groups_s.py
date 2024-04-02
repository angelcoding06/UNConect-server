from rest_framework.serializers import ModelSerializer
from groups.models import Groups

class GroupsSerielizer(ModelSerializer):
    class Meta: 
        model = Groups
        fields = '__all__'