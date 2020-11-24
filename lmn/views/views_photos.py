from django.shortcuts import render, redirect

from ..models import Show
from ..forms import PhotosForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

@login_required
def add_photo(request):
    if request.method == 'POST':
        # Need POST and FILES so photo image file is saved to database.
        form = PhotosForm(request.POST , request.FILES)
        photo = form.save(commit=False) # Do I need an "instance=x" here?
        photo.user = request.user
        # If valid, saves photo file and retuns user to "homepage" to view updated page.
        if form.is_valid():
            photo.save()
            return redirect('homepage')
    # Updates photos_form and add_photo.html
    photos_form = PhotosForm()
    return render(request , 'lmn/add_photo.html' , {'photos_form' : photos_form})
