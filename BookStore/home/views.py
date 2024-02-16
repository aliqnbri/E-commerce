from django.shortcuts import render
from django.views.generic.base import TemplateView
from home.models import ShopInfo

# Create your views here.

class IndexView(TemplateView):
    template_name = 'home/index.html'  
    context_object_name = 'shopinfo'  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["shopinfo"] = ShopInfo.objects.all()
        return context
    