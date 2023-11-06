$(document).ready(function() {
    // Function to post a question to the server
    function askQuestion() {
        var question = $('#question').val();
        $.ajax({
            url: '/ask',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ 'question': question }),
            success: function(response) {
                $('#chat-history').append('<p><strong>You:</strong> ' + question + '</p>');
                $('#chat-history').append('<p><strong>Bot:</strong> ' + response + '</p>');
                $('#question').val(''); // Clear the input field
            }
        });
    }

    // Function to clear the chat history
    function clearHistory() {
        $.ajax({
            url: '/clear_history',
            type: 'POST',
            success: function(response) {
                $('#chat-history').empty();
            }
        });
    }

    // Event handler for the 'Ask' button
    $('#ask-button').click(function() {
        askQuestion();
    });

    // Event handler for pressing 'Enter' in the question field
    $('#question').keypress(function(event) {
        if (event.which == 13) { // Enter key has a keycode of 13
            askQuestion();
        }
    });

    // Event handler for the 'Clear History' button
    $('#clear-history').click(function() {
        clearHistory();
    });
});
