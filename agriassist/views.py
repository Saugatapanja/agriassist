from django.http import HttpResponse
from django.shortcuts import render
import joblib
import numpy as np
from keras.models import load_model
from keras.preprocessing import image
from django.core.files.storage import FileSystemStorage

class_names = ['Apple___Apple_scab',
                   'Apple___Black_rot',
                   'Apple___Cedar_apple_rust',
                   'Apple___healthy',
                   'Blueberry___healthy',
                   'Cherry_(including_sour)___Powdery_mildew',
                   'Cherry_(including_sour)___healthy',
                   'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
                   'Corn_(maize)___Common_rust_',
                   'Corn_(maize)___Northern_Leaf_Blight',
                   'Corn_(maize)___healthy',
                   'Grape___Black_rot',
                   'Grape___Esca_(Black_Measles)',
                   'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
                   'Grape___healthy',
                   'Orange___Haunglongbing_(Citrus_greening)',
                   'Peach___Bacterial_spot',
                   'Peach___healthy',
                   'Pepper,_bell___Bacterial_spot',
                   'Pepper,_bell___healthy',
                   'Potato___Early_blight',
                   'Potato___Late_blight',
                   'Potato___healthy',
                   'Raspberry___healthy',
                   'Soybean___healthy',
                   'Squash___Powdery_mildew',
                   'Strawberry___Leaf_scorch',
                   'Strawberry___healthy',
                   'Tomato___Bacterial_spot',
                   'Tomato___Early_blight',
                   'Tomato___Late_blight',
                   'Tomato___Leaf_Mold',
                   'Tomato___Septoria_leaf_spot',
                   'Tomato___Spider_mites Two-spotted_spider_mite',
                   'Tomato___Target_Spot',
                   'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
                   'Tomato___Tomato_mosaic_virus',
                   'Tomato___healthy']


def home(request):
    return render(request,"index.html")
def crop_recommend(request):
    return render(request,"crop_recommend.html")
def crop_recommend_result(request):
    # Filter out non-integer values
    features = [int(x) for x in request.POST.values() if x.isdigit()]
    arr = [np.array(features)]
    print(arr)
    model = joblib.load("crop_recommend.joblib")
    pred = model.predict(arr)
    print(pred)
    return render(request, 'crop_recommend_result.html', {'data': pred})

def crop_disease(request):
    return render(request,"crop_disease.html")

def crop_disease_result(request):
    fileobj=request.FILES["filePath"]
    fs=FileSystemStorage()
    filePathName=fs.save(fileobj.name, fileobj)
    filePathName=fs.url(filePathName)
    model = load_model("crop_disease.h5")
    test_image='.'+ filePathName
    # img = Image.open(img_path)
    # img = img.resize((120, 120))
    img=image.load_img(test_image,target_size=(120,120))
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    probs = model.predict(img)[0]

    # Get the predicted class index and name
    pred_class_prob = np.argmax(probs)
    pred_class_name = class_names[pred_class_prob]

    max_prob = np.max(probs)
    print(f'Predicted class: {pred_class_name}')
    print(f'Maximum probability: {max_prob}')
    context={'filePathName':filePathName,'predictedLabel':pred_class_name}
    return render(request,"crop_disease.html",context)

def fertilizer_recommend(request):
    return render(request,"fertilizer_recommend.html")

def fertilizer_recommend_result(request):
    if request.method == 'POST':
        # Get the values of nitrogen, phosphorus, and potassium from the form
        try:
            temp = int(request.POST['a'])
            humi = int(request.POST['b'])
            mois = int(request.POST['c'])
            N = int(request.POST['d'])
            K = int(request.POST['e'])
            P = int(request.POST['f'])            
            soil=int(request.POST['g'])
            crop=int(request.POST['h'])

        except ValueError:
            # Handle the case where the submitted values are not integers
            return render(request,{'error_message': 'Please enter all values'})

        # Create a feature array from the input values
        features = [temp, humi, mois, soil, crop, N, K, P]
        arr = [np.array(features)]

        # Load the pre-trained ML model
        model = joblib.load("fertilizer.joblib")

        # Make predictions using the model
        pred = model.predict(arr)
        print(pred)
        # Render the result template with the prediction
        return render(request, 'fertilizer_recommend_result.html', {'data': pred})
    
