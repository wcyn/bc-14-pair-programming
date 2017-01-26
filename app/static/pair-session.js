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
                var firepadRef = getExampleRef(data['uid']);

                // get chats for this session and populate ui
                // prepopulateChatSpace(getChats(firepadRef.key));
                updateChatSpace(firepadRef.key);

                user_details.uid = data['uid'];
                var userRef = firebase.database().ref('users/' + data['uid'] + '/username/');
                var firepad = Firepad.fromCodeMirror(firepadRef, codeMirror, {
                    defaultText: '# Welcome to Psquair: Start writing some Python Code\nprint("Hello World!")\n',
                    userId: data['uid']
                });
                userRef.on('value', function(snapshot) {
                    //   updateStarCount(postElement, snapshot.val());
                    console.log("Snapshot stringified: " +
                    String(snapshot.val()).charAt(0));
                    //   updateUIElement("aside #sidebar .sidebar-menu #current-user .name-initial"
                    //   ).text(snapshot.val())
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
    console.log("Chat Sending...");
    // Reference to the /chats/ database path.
    var chatsRef = firebase.database().ref().child('chats').child(sessionId);
    console.log("Chat Sending after ref");
    var data = {
        message: message,
        userId: userId
    };
    console.log("Chat Sending starting...");
    chatsRef.push(data);
    console.log("Chat Sending Finished");

};

// Reteieve all chats once
function getChats(sessionId) {
    console.log("Getting chats...");
    var chatsRef = firebase.database().ref().child('chats').child(
        sessionId);
    chatsRef.once('value', function(snapshot) {
        console.log("Chat snapshot get all: " + JSON.stringify(snapshot.val()));
        return snapshot.val();
    });
}

function getNewChats(sessionId) {
    console.log("Getting chats...");
    var chatsRef = firebase.database().ref().child('chats').child(
        sessionId);
    chatsRef.on('child_added', function(snapshot) {
        console.log("Chat snapshot new chats: " + snapshot.val()['message']);
        return snapshot.val();
    });
}

function prepopulateChatSpace(snapchat_obj) {
    for (var key in snapchat_obj) {
        console.log("json loop..");
      if (snapchat_obj.hasOwnProperty(key)) {
        console.log(key + " -> " + JSON.stringify(snapchat_obj[key]['message']));
        updateChatSpace(JSON.stringify(snapchat_obj[key]['message']))
      } else{
          console.log("Nothing in json loop..");
      };
    }
}

// Update chat space with messages
function updateChatSpace(sessionId) {
    console.log("Getting chats...");
    var chatsRef = firebase.database().ref().child('chats').child(
        sessionId);
    chatsRef.on('child_added', function(snapshot) {
        console.log("Chat snapshot new chats: " + snapshot.val()['message']);
        var chat_obj = snapshot.val();
        if (chat_obj) {
        console.log("Updating chat space..: " + chat_obj);
        $('#sidebar-chat .sidebar-chat-list').each(function(){
            $('<li />', {
                class : 'chat-msg',
                text: chat_obj['message'],
                appendTo : this
            });
        });
    } else {
        console.log("NO chat object")
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
