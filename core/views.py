import numpy as np
import requests
from django.conf import settings
from django.core.files.storage import default_storage
from django.shortcuts import render
from keras.applications import vgg16
from keras.applications.imagenet_utils import decode_predictions
from keras.preprocessing.image import img_to_array, load_img
from tensorflow.python.keras.backend import set_session

def index(request):
    return render(request, "index.html")
    
def classify(request):
    if request.method != "POST":
        return render(request, "index.html")
    #
    # Django image API
    #
    file = request.FILES["imageFile"]
    file_name = default_storage.save(file.name, file)
    file_url = default_storage.path(file_name)

    #
    # https://www.tensorflow.org/api_docs/python/tf/keras/preprocessing/image/load_img
    #
    image = load_img(file_url, target_size=(224, 224))
    numpy_array = img_to_array(image)
    image_batch = np.expand_dims(numpy_array, axis=0)
    processed_image = vgg16.preprocess_input(image_batch.copy())

    #
    # get the predicted probabilities
    #
    with settings.GRAPH1.as_default():
        set_session(settings.SESS)
        predictions = settings.IMAGE_MODEL.predict(processed_image)

    #
    # Output/Return data
    #

    label = decode_predictions(predictions, top=9)[0]

    data = []

    url = "https://pexelsdimasv1.p.rapidapi.com/v1/search"

    for i in label:  
        query = i[1].replace("_"," ")  

        querystring = {"query":query,"locale":"en-US","per_page":"1","page":"1"}

        headers = {
            'authorization': "563492ad6f91700001000001692697fded6c41cb9d80c43577e2d08a",
            'x-rapidapi-host': "PexelsdimasV1.p.rapidapi.com",
            'x-rapidapi-key': "934e2328d9msh9e6f388587d46d0p10d8d4jsnad491ee8fa2d"
            }

        response = requests.request("GET", url, headers=headers, params=querystring).json()
        picture_list = response['photos']
        picture = "https://images.pexels.com/photos/3683107/pexels-photo-3683107.jpeg?auto=compress&cs=tinysrgb&dpr=3&h=750&w=1260"

        if len(picture_list) != 0:
            picture = picture_list[0]['src']['original']

        new_t = (i[0], query.capitalize(), round(i[2]*100, 2), picture)
        data.append(new_t)

    print(data)

    return render(request, "index.html", {"predictions": data})