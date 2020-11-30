from django.shortcuts import render, redirect, get_object_or_404

from ..models import Venue, Artist, Note, Show, Photo
from ..forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm, PhotosForm, # INCLUDE SHOW FORM WHEN AVAILABLE!

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

@login_required
def add_photo(request, show_pk):
    
    show = get_object_or_404(Show, pk=show_pk)

    if request.method == 'POST':
        form = PhotosForm(request.POST , request.FILES , instance=Photo)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.show = show
            photo.save()
            messages.info(request, 'Your photo has been added!')
            return redirect('lmn/photos/show_photos.html', photo_pk=photo.pk)
        else:
            messages.error(request , form.errors)
        return redirect('lmn/photos/show_photos.html')
    else:
        form = PhotosForm()

    return render(request, 'lmn/photos/show_photos.html' , { 'form': form , 'show': show })
