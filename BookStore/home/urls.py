from django.urls import path ,include
from home.views import index_view

urlpatterns = [
   path('', index_view)
 
   
]