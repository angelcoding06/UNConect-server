from rest_framework.serializers import ModelSerializer
from groups.models import Persons

class PersonsSerielizer(ModelSerializer):
    class Meta:
        model = Persons
        fields = '__all__' 

