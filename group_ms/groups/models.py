from django.db import models

# Create your models here.
class Persons(models.Model):
    user_id = models.CharField(max_length=200)

    def __str__(self):
        return self.user_id
    

class Groups(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    owner_id = models.ForeignKey(Persons, on_delete=models.CASCADE)
    in_requests = models.ManyToManyField(Persons, related_name='solicitudes')
    members = models.ManyToManyField(Persons, related_name='miembros')
    admins = models.ManyToManyField(Persons, related_name='administradores')
    is_private = models.BooleanField()
    
    def __str__(self):
        return self.name

