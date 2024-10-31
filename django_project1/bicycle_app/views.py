from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
from django.template import loader

def index(request):
    #return HttpResponse("Hello world from bicycle_app!")
    product_item = Product.objects.all()
    context = {'product_item': product_item}
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))
