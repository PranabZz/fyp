import os
import pickle
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, HttpResponseRedirect, reverse
from .models import ImageCaption
from django.db.models import Count
from django import forms
import tensorflow as tf
import numpy as np

# load pre-trained model and tokenizer
model = tf.keras.models.load_model('D:/Yep/Study/Herald/Semester 5/6CS007 - Project and Professionalism/Captionify/Website/Models/model_vgg16.h5')
vgg_model = tf.keras.applications.vgg16.VGG16()
vgg_model = tf.keras.models.Model(inputs=vgg_model.inputs, outputs=vgg_model.layers[-2].output)
with open('D:/Yep/Study/Herald/Semester 5/6CS007 - Project and Professionalism/Captionify/Website/tokenizer.pkl', 'rb') as f:
    tokenizer = pickle.load(f)

# define maximum caption lengths
max_length = 35

class ImageCaptionForm(forms.ModelForm):
    class Meta:
        model = ImageCaption
        fields = '__all__'

def upload_image(request):
    user = request.user
    caption = None
    image_path = None
    if request.method == 'POST':
        image_file = request.FILES['image-file']
        # save uploaded image to media folder
        image_path = os.path.join(settings.MEDIA_ROOT, image_file.name)
        with open(image_path, 'wb+') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)

        # save uploaded image to ImageCaption model in Django admin
        image_caption = ImageCaption.objects.create(image=image_file)

        # load and preprocess image
        image = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
        image = tf.keras.preprocessing.image.img_to_array(image)
        image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
        image = tf.keras.applications.vgg16.preprocess_input(image)
        
        # extract features using VGG16 model
        feature = vgg_model.predict(image, verbose=0)
        
        # generate caption using pre-trained model
        caption = generate_caption(model, feature, tokenizer, max_length)

        # update caption field of ImageCaption model
        image_caption.caption = caption
        image_caption.save()

    return render(request, 'upload.html', {'caption': caption, 'image_path': image_path, 'user':user})
    
def generate_caption(model, feature, tokenizer, max_length):
    # start the caption with the start token
    caption = 'startseq'
    for i in range(max_length):
        # tokenize the caption sequence
        sequence = tokenizer.texts_to_sequences([caption])[0]
        # pad the sequence
        sequence = tf.keras.preprocessing.sequence.pad_sequences([sequence], maxlen=max_length)
        # predict next word using pre-trained model
        yhat = model.predict([feature, sequence], verbose=0)
        # convert probability to integer index
        yhat = np.argmax(yhat)
        # map integer index to word
        word = word_for_id(yhat, tokenizer)
        # stop caption generation if end token is encountered
        if word is None:
            break
        caption += ' ' + word
        # stop caption generation if end token is encountered
        if word == 'endseq':
            break
    return caption.replace('startseq', '').replace('endseq', '')

def word_for_id(integer, tokenizer):
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None

@login_required
def browse_captions(request):
    sort = request.GET.get('sort')
    if sort == 'likes':
        images = ImageCaption.objects.all().order_by('-likes', '-created_at')
    elif sort == 'created':
        images = ImageCaption.objects.all().order_by('-created_at')
    else:
        images = ImageCaption.objects.all()
    return render(request, 'browse.html', {'images': images})

@login_required
def like_image(request, image_caption_id):
    image_caption = get_object_or_404(ImageCaption, id=image_caption_id)
    if request.user.is_authenticated:
        if request.user in image_caption.likes.all():
            image_caption.unlike(request.user)
        else:
            image_caption.like(request.user)
    return HttpResponseRedirect(reverse('myapp:browse_captions'))
