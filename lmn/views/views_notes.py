from django.shortcuts import render, redirect, get_object_or_404

from ..models import Venue, Artist, Note, Show
from ..forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm, NoteSearchForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseForbidden
from django.contrib import messages

@login_required
def new_note(request, show_pk):

    show = get_object_or_404(Show, pk=show_pk)  # If no note found, display 404 error

    # Saves completed note form fields as a note and creates a new note_detail page
    if request.method == 'POST':
        form = NewNoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.show = show
            note.save()
            messages.info(request, 'Note Successfully Added/Updated')
            # Returns note_detail.html page with details for a specific note about a specific show
            return redirect('note_detail', note_pk=note.pk)
    else :
        # Allows users to add a new note for a specific show
        form = NewNoteForm()
    # Returns new_note.html page with form
    return render(request, 'lmn/notes/new_note.html' , { 'form': form , 'show': show })

@login_required
def notes_search(request):

    # Allows users to search for a specific note from all existing notes
    form = NoteSearchForm()
    search_name = request.GET.get('search_name') # Search term entered by user

    if search_name:
        # If serach term matches an existing note(s), display all matching notes ordered by search term
        notes = Note.objects.filter(title__icontains=search_name).order_by('-posted_date')
    else:
        # Otherwise display all existing notes for all shows, ordered by posted date
        notes = Note.objects.all().order_by('-posted_date')

    # Returns note_list.html page with all search-specific notes
    return render(request, 'lmn/notes/note_list.html', { 'notes': notes, 'form': form, 'search_term': search_name })

@login_required
def latest_notes(request):

    # Allows users to search for a specific note from all existing notes using code in views_notes.notes_search function
    form = NoteSearchForm()
    notes = Note.objects.all().order_by('-posted_date') # All existing notes for all shows, ordered by posted date

    # Returns note_list.html page with all existing notes, ordered by posted date
    return render(request, 'lmn/notes/note_list.html', { 'notes': notes, 'form': form })

@login_required
def notes_for_show(request, show_pk):

    # Allows users to search for a specific note from all existing notes using code in views_notes.notes_search function
    form = NoteSearchForm()
    show = Show.objects.get(pk=show_pk) # Identifies specific existing show
    notes = Note.objects.filter(show=show_pk).order_by('-posted_date')  # All existing notes for specific show, ordered by posted date

    # Returns note_list.html page with all show-specific notes, ordered by posted date
    return render(request, 'lmn/notes/note_list.html', { 'show': show, 'notes': notes, 'form': form })

@login_required
def note_detail(request, note_pk):

    note = get_object_or_404(Note, pk=note_pk) # If no note found, display 404 error

    # Returns note_detail.html page with details for a specific note about a specific show
    return render(request, 'lmn/notes/note_detail.html' , { 'note': note })
