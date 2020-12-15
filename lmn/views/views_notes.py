from django.shortcuts import render, redirect, get_object_or_404

from ..models import Venue, Artist, Note, Show
from ..forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm, NoteSearchForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseForbidden, HttpResponse
from django.contrib import messages

from django.core.paginator import Paginator

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
            messages.info(request, 'Note Successfully Added!')

            # Returns note_detail.html page with details for a specific note about a specific show
            return redirect('note_detail', note_pk=note.pk)
    else :
        # Allows users to add a new note for a specific show
        form = NewNoteForm()

    # Returns new_note.html page with form
    return render(request, 'lmn/notes/new_note.html' , { 'form': form ,  'show': show })

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
    paginator = Paginator(notes,5)

        #it will default grab page 1
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        notes = paginator.page(page)
    except:
        notes = paginator.page(paginator.num_pages)
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


@login_required
def delete_notes(request, note_pk):

    """If this is a note user request, the user clicked the Delete button
    in the form. Delete note to the 
    database, and redirect to this same page.

    If note is not valid, display an url response forbidden. 
    """
    note = get_object_or_404(Note, pk=note_pk) 
    if note.user == request.user:
        note.delete() # Delete to the database
        return redirect('venue_list')
    else:
        return HttpResponseForbidden()

@login_required
def edit_notes(request, note_pk):

    """User requests to edit notes by clicking on Edit button.
    User with valid primary key can edit notes in database
    and redirect to starting page. 

    Whereas, invalid primary key will show forbidden information.
    """
    note = get_object_or_404(Note, pk=note_pk) # Return error code and primary key if note not found
    
    # Does this note belong to the current user?
    if note.user != request.user:
        return HttpResponseForbidden()
    
    # is this a GET request (showdata + form), or a POST request (update Note object)?
    # if POST request, validate form data and update.
    if request.method == 'POST':
        form = NewNoteForm(request.POST, instance=note)
        
        if form.is_valid(): # confirm form
            form.save() 
            messages.info(request, 'Note information update!')
        else:
            messages.error(request, form.errors)
        
        return redirect('note_detail', note_pk=note_pk)
    
    else:
    # If GET request, show Note information and form.
    # If Note is edited, show form; if note is not edited, no form
        if note:
            form = NewNoteForm(instance=note)# get new form
            return render(request, 'lmn/notes/note_edit.html' , { 'form': form, 'note': note})
        
        else:
            return render(request, 'lmn/notes/note_edit.html' ,  { 'form': form})
