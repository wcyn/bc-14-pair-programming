/* global firebase, Firepad, $, CodeMirror, FirepadUserList */

function init() {
    //// Initialize Firebase.
    var config = {
        apiKey: "AIzaSyDzBN-pfGvMGR1aIsjTkXEehavEN1TDZMs",
        authDomain: "psqair.firebaseapp.com",
        databaseURL: "https://psqair.firebaseio.com"
    };

    var firepad = null, codeMirror = null, userList = null;
    if (firepad) {
      // Clean up.
      firepad.dispose();
      userList.dispose();
      $('.CodeMirror').remove();
    }
    $(document).ready(function() {
        $.ajax({
            url: "/api/user_token"
        }).then(function(token_data) {
            firebase.initializeApp(config);
            var user_details = {
                username: "",
                uid:""
            }

            //// Create CodeMirror (with line numbers and the JavaScript mode).
            var codeMirror = CodeMirror(document.getElementById('firepad-container'), {
                lineNumbers: true,
                lineWrapping: true,
                mode:'python',
                theme: "monokai",
                indentWithTabs: true
            });
            firebase.auth().signInWithCustomToken(token_data['token']).then(function(data) {
                // Authentication successful.
                // Enable send chat message button
                $('#sidebar-chat #chat-input #send-chat-btn').prop('disabled', false);
                // Create an on click listener for the button
                $('#sidebar-chat #chat-input #chat-field').keypress(function(e) {
                    if(e.which == 13) {
                        $(this).blur();
                        $('#sidebar-chat #chat-input #send-chat-btn').focus().click();
                    }
                });
                // on click listener for sned button
                $('#sidebar-chat #chat-input #send-chat-btn').click( function() {
                    var message = $('#sidebar-chat #chat-input #chat-field').val();
                    sendChat(firepadRef.key, message, data['uid']);
                    //  Empty the input area for new message
                    $('#sidebar-chat #chat-input #chat-field').val('');
                });
                //// Get Firebase Database reference.
                var user_id = window.location.pathname.split("/").pop()
                var firepadRef = getExampleRef(user_id);

                // get chats for this session and populate ui
                updateChatSpace(user_id, firepadRef.key);

                user_details.uid = data['uid'];
                var userRef = firebase.database().ref('users/' + data['uid'] + '/username/');
                var firepad = Firepad.fromCodeMirror(firepadRef, codeMirror, {
                    defaultText: '# Welcome to Psquair: Start writing some Python Code\nprint("Hello World!")\n',
                    userId: data['uid']
                });
                userRef.on('value', function(snapshot) {
                    console.log("Snapshot stringified: " +
                    String(snapshot.val()).charAt(0));
                    var username = String(snapshot.val())
                    var init_char = username.charAt(0)
                    $("#sidebar .sidebar-menu #current-user .name-initial").text(init_char);
                    $("#sidebar .sidebar-menu #current-user .u-name").text(username);
                    var userList = FirepadUserList.fromDiv(firepadRef.child('users'),
                    document.getElementById('firepad-userlist'), data['uid'], username);
                });

            }, function(error) {
                var errorCode = error.code;
                var errorMessage = error.message;
                console.log(error)
            });

            codeMirror.focus();
        });
    });

}

// Send chat message to Firebase.
function sendChat(sessionId, message, userId) {
    // Reference to the /chats/ database path.
    var chatsRef = firebase.database().ref().child('chats').child(sessionId);
    var data = {
        message: message,
        userId: userId
    };
    chatsRef.push(data);

};


// Load chat space with messages
function loadChatSpace(userId, sessionId) {
    console.log("Getting chats...");
    var chatsRef = firebase.database().ref().child('chats').child(
        sessionId);

    chatsRef.once('value', function(snapshot) {
        var chat_obj = snapshot.val();
        snapshot.forEach(function(childSnapshot) {
            var childData = childSnapshot.val();
            console.log("Chat childData: " + JSON.stringify(childData['message']));
            if (childData) {
                var sessionChatRef = firebase.database().ref().child('pair_sessions').child(
                    userId).child(sessionId).child('users').child(
                    childData['userId']);
                console.log("Appending from load");
                $('#sidebar-chat .sidebar-chat-list').empty();
                sessionChatRef.on("value", function(sessSnapshot){
                    var username = sessSnapshot.val()['name']
                    var color = sessSnapshot.val()['color']
                    console.log("Username: " + username);
                    $('<li class="chat-content">'
                        + '<div class="div-circle" style="background-color:'
                        + color + ';">'
                        + username.charAt(0)
                        + '</div>'
                        + '<div class="msg-details">'
                        + '<div class="sender-name">'
                        + username
                        + '</div>'
                        + '<p class="chat-msg">'
                        + childData['message']
                        + '</p>'
                        + '</div>'
                        + '</li>'
                    ).appendTo('#sidebar-chat .sidebar-chat-list');
                });
                } else {
                console.log("No chat object");
                }
          });
    });

}

// Load chat space with messages
function updateChatSpace(userId, sessionId) {
    var chatsRef = firebase.database().ref().child('chats').child(
        sessionId);

    chatsRef.on('child_added', function(snapshot) {
        var chat_obj = snapshot.val();
        console.log("Chat sobject: " + JSON.stringify(chat_obj));
        if (chat_obj) {
            console.log("Chat childobj: " + JSON.stringify(chat_obj['message']));
            console.log("Chat object new chats: " + JSON.stringify(chat_obj['message']));
            var sessionChatRef = firebase.database().ref().child('pair_sessions').child(
                userId).child(sessionId).child('users').child(
                chat_obj['userId']);

            sessionChatRef.once("value", function(sessSnapshot){
                var username = sessSnapshot.val()['name']
                var color = sessSnapshot.val()['color']
                console.log("Username: " + username);
                $('<li class="chat-content">'
                    + '<div class="div-circle" style="background-color:'
                    + color + ';">'
                    + username.charAt(0)
                    + '</div>'
                    + '<div class="msg-details">'
                    + '<div class="sender-name">'
                    + username
                    + '</div>'
                    + '<p class="chat-msg">'
                    + chat_obj['message']
                    + '</p>'
                    + '</div>'
                    + '</li>'
                ).appendTo('#sidebar-chat .sidebar-chat-list');
            });
            } else {
            console.log("No chat object");
            }
          });
}

// Helper to get hash from end of URL or generate a random one.
function getExampleRef(userId) {
    var ref = firebase.database().ref().child('pair_sessions').child(userId);
    var hash = window.location.hash.replace(/#/g, '');
    if (hash) {
        ref = ref.child(hash);
    } else {
        ref = ref.push(); // generate unique location.
        window.location = window.location + '#' + ref.key; // add it as a hash to the URL.
    }
    if (typeof console !== 'undefined') {
        console.log('Firebase data: ', ref.toString());
    }
    return ref;
}
