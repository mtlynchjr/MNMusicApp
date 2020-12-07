from django.shortcuts import render, redirect, get_object_or_404

from ..models import Venue, Artist, Note, Show
from ..forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import AddForm


@login_required
def new_note(request, show_pk):

    show = get_object_or_404(Show, pk=show_pk)

    if request.method == 'POST' :
        form = NewNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.show = show
            note.save()
            return redirect('note_detail', note_pk=note.pk)

    else :
        form = NewNoteForm()

    return render(request, 'lmn/notes/new_note.html' , { 'form': form , 'show': show })


def latest_notes(request):
    notes = Note.objects.all().order_by('-posted_date')
    return render(request, 'lmn/notes/note_list.html', { 'notes': notes })


def notes_for_show(request, show_pk): 
    # Notes for show, most recent first
    notes = Note.objects.filter(show=show_pk).order_by('-posted_date')
    show = Show.objects.get(pk=show_pk)  
    return render(request, 'lmn/notes/note_list.html', { 'show': show, 'notes': notes })


def note_detail(request, note_pk):
    note = get_object_or_404(Note, pk=note_pk)
    return render(request, 'lmn/notes/note_detail.html' , { 'note': note })

def add_note(request):
    if request.method == 'POST':
        n_note_form = AddForm(request.POST)
        if n_note_form.is_valid():
           n_note_form.save()
        else:
            return render(request, 'lmn/notes/add_note.html', {'n_note_form ': n_note_form })

    n_note_form = AddForm()
    return render(request, 'lmn/notes/add_note.html', {'n_note_form ': n_note_form })

