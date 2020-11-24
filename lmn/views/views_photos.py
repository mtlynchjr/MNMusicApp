from django.shortcuts import render, redirect, get_object_or_404

from ..models import Photo, Show
from ..forms import PhotosForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

@login_required
def add_photo(request, show_pk):
    
    show = get_object_or_404(Show, pk=show_pk)

    if request.method == 'POST':
        # Needs FILES in addition to POST so photo image file is saved.
        form = PhotosForm(request.POST , request.FILES)
        if form.is_valid():
            photo = form.save(commit=False) # Do I need an "instance=x" here?
            photo.user = request.user
        # If valid, saves photo file and returns user to updated page.
        photo.show = show
        photo.save()
        return redirect('photo_detail', photo_pk=photo.pk)
    else:
        form = PhotosForm()

        return render(request, 'lmn/photos/add_photo.html' , { 'form': form , 'show': show })

@login_required
def photo_detail(request, photo_pk):
    photo = get_object_or_404(Photo, pk=photo_pk)
    return render(request, 'lmn/photos/photo_detail.html' , { 'photo': photo })

@login_required
def show_photos(request, show_pk): 
    # Photos for a specific show
    photos = Photo.objects.filter(show=show_pk).order_by('-photo_str')
    show = Show.objects.get(pk=show_pk)  
    return render(request, 'lmn/photos/photo_list.html', { 'show': show, 'photos': photos })
