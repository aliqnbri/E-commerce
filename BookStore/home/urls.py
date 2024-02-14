from django.urls import path ,include
from home.views import IndexView

urlpatterns = [
   path('', IndexView.as_view(),)
 
   
]