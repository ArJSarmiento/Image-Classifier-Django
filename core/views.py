import numpy as np
import requests

from django.conf import settings 
from django.core.files.storage import default_storage
from rest_framework import status

from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view

from keras.applications import vgg16
from keras.applications.imagenet_utils import decode_predictions
from keras.preprocessing.image import img_to_array, load_img
from tensorflow.python.keras.backend import set_session


@api_view(['GET'])
def index():
    data = {
        'name': 'Arnel Jan Sarmiento',
        'job': 'Software Engineer',
    }
    return Response(data)

@api_view(["POST"])
def classify(request):
    try:
        file = request.FILES["imageFile"]
        file_name = default_storage.save(file.name, file)
        file_url = default_storage.path(file_name)
        image = load_img(file_url, target_size=(224, 224))
        numpy_array = img_to_array(image)
        image_batch = np.expand_dims(numpy_array, axis=0)
        processed_image = vgg16.preprocess_input(image_batch.copy())
        with settings.GRAPH1.as_default():
            set_session(settings.SESS)
            predictions = settings.IMAGE_MODEL.predict(processed_image)
        label = decode_predictions(predictions, top=9)[0]
        data = []
        url = "https://pexelsdimasv1.p.rapidapi.com/v1/search"
        for i in label:
            query = i[1].replace("_", " ")
            querystring = {"query": query, "locale": "en-US", "per_page": "1", "page": "1"}
            headers = {'authorization': "563492ad6f91700001000001692697fded6c41cb9d80c43577e2d08a", 'x-rapidapi-host': "PexelsdimasV1.p.rapidapi.com", 'x-rapidapi-key': "934e2328d9msh9e6f388587d46d0p10d8d4jsnad491ee8fa2d"}

            response = requests.request("GET", url, headers=headers, params=querystring).json()

            picture_list = response['photos']
            picture = "https://images.pexels.com/photos/3683107/pexels-photo-3683107.jpeg?auto=compress&cs=tinysrgb&dpr=3&h=350&w=467"

            if len(picture_list) != 0:
                picture = picture_list[0]['src']['original']
            new_t = {'id': i[0], 'title': query.capitalize(), 'certainty': round(i[2] * 100, 2), 'picture': picture}

            data.append(new_t)
        return JsonResponse(data, safe=False)
    except Exception:
        return Response(status=status.HTTP_400_BAD_REQUEST)