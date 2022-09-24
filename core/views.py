import requests

from django.conf import settings 
from django.core.files.storage import default_storage
from rest_framework import status

from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
import environ
env = environ.Env()
environ.Env.read_env()

@api_view(['GET'])
def index(request):
    data = {
        'name': 'Arnel Jan Sarmiento',
        'job': 'Intermediate Full-stack Web Developer',
    }
    return Response(data)

@api_view(["POST"])
def classify(request):
    try:
        file = request.FILES["imageFile"]
        file_name = default_storage.save(file.name, file)
        file_url = default_storage.path(file_name)
        response = requests.post(
            'https://api.imagga.com/v2/tags',
            auth=(env('IMAGGA_API_KEY'), env('IMAGGA_API_SECRET')),
            files={'image': open(file_url, 'rb')})
        
        return Response(response.json())
    except Exception:
        return Response(status=status.HTTP_400_BAD_REQUEST)