from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import tensorflow as tf
import numpy as np

# Load the pre-trained model
model = tf.keras.models.load_model('./Website/Models/model_dense.h5')

def upload_image(request):
    if request.method == 'POST' and request.FILES['image-file']:
        # Get the uploaded image
        image_file = request.FILES['image-file']
        # Save the image to a temporary location
        fs = FileSystemStorage()
        filename = fs.save(image_file.name, image_file)
        uploaded_file_url = fs.url(filename)
        # Load the image into a NumPy array
        img = tf.keras.preprocessing.image.load_img(uploaded_file_url, target_size=(224, 224))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        # Generate a caption for the image using the pre-trained model
        caption = model.predict(img_array)[0]
        # Pass the caption to the template context
        context = {'caption': caption}
        return render(request, 'upload.html', context)
    return render(request, 'upload.html')
