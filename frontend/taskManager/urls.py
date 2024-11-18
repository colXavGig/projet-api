from django.urls import path
from . import views as v

urlpatterns = [
    path("assigned-to/", v.get_assigned_task, name="assignedTo"),
    path('created-by/', v.get_created_task, name='createdBy'),
    path('<str:pathForRedirect>/<str:id>', v.manage_task, name='manageTask'),
]
