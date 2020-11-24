from django.shortcuts import render, redirect

from ..models import Photo
from ..forms import PhotosForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

@login_required
def add_photo(request, photo_pk):
    if request.method == 'POST':
        # Needs FILES in addition to POST so photo image file is saved.
        form = PhotosForm(request.POST , request.FILES)
        photo = form.save(commit=False) # Do I need an "instance=x" here?
        photo.user = request.user
        # If valid, saves photo file and returns user to updated page.
        if form.is_valid():
            photo.save()
            return redirect('home')
    # Updates photos_form and add_photo.html
    photos_form = PhotosForm()
    return render(request , 'lmn/photos/add_photo.html' , {'photos_form' : photos_form})
