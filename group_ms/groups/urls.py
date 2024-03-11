from django.urls import path
from groups.views.persons_v import getPerson,postPerson,putPerson,deletePerson
from groups.views.groups_v import getGroup,postGroup,deleteGroup,putGroup, add_member, add_in_request, delete_member,delete_admin, add_admin, delete_in_request
urlpatterns=[
    path('getPerson/', getPerson),
    path('postPerson/', postPerson),
    path('putPerson/<int:pk>/', putPerson),
    path('deletePerson/<int:pk>/', deletePerson),
    path('getGroup/', getGroup),
    path('postGroup/',postGroup),
    path('putGroup/<int:pk>/', putGroup),
    path('deleteGroup/<int:pk>/', deleteGroup),
    path('add_member/<int:pk>/', add_member),
    path('add_in_request/<int:pk>/', add_in_request),
    path('delete_in_request/<int:group_id>/<int:in_request_id>/', delete_in_request ),
    path('delete_member/<int:group_id>/<int:member_id>/', delete_member),
    path('delete_admin/<int:group_id>/<int:admin_id>/', delete_admin),
    path('add_admin/<int:pk>/', add_admin),

    


]
