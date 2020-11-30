var deleteButtons = document.querySelectorAll('.delete');

// Create a delete event listener
deleteButtons.forEach(function(button){
    button.addEventListener('click', function(ev){
        // Prompt user to confirm note deletion
        var okToDelete = confirm("Are you sure you want to delete this photo?");
        
        // Prevent form submission if user declines deletion
        if (!okToDelete) {
            ev.preventDefault();  // Prevent deletion event
        }
        // If user confirms deletion, note deletion will occur as requested
    })
});
