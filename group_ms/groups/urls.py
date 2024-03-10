from django.urls import path
from groups.views.persons_v import getPerson,postPerson,putPerson,deletePerson
from groups.views.groups_v import getGroup
urlpatterns=[
    path('getPerson/', getPerson),
    path('postPerson/', postPerson),
    path('putPerson/<int:pk>/', putPerson),
    path('deletePerson/<int:pk>/', deletePerson),
    path('getGroup/', getGroup)

    


]
