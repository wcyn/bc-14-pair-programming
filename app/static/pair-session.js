/* global firebase, Firepad, $, CodeMirror */

function init() {
    //// Initialize Firebase.
    var config = {
        apiKey: "AIzaSyDzBN-pfGvMGR1aIsjTkXEehavEN1TDZMs",
        authDomain: "psqair.firebaseapp.com",
        databaseURL: "https://psqair.firebaseio.com"
    };

    $(document).ready(function() {
        $.ajax({
            url: "/api/user_token"
        }).then(function(token_data) {
            console.log("Data from API: " + JSON.stringify(token_data));
            // var cust_token = data['token']
            // console.log("Cust token: " + cust_token)
            firebase.initializeApp(config);
            //// Get Firebase Database reference.
            var firepadRef = getExampleRef();
            //// Create CodeMirror (with line numbers and the JavaScript mode).
            var codeMirror = CodeMirror(document.getElementById('firepad-container'), {
                lineNumbers: true,
                mode: 'javascript'
            });
            firebase.auth().signInWithCustomToken(token_data['token']).then(function(data) {
                // Authentication successful.
                console.log("Authentication successful!");
                console.log("Data: " + JSON.stringify(data));

            }, function(error) {
                var errorCode = error.code;
                var errorMessage = error.message;
                console.log(error)
            });
            var user = firebase.auth().currentUser;
            console.log("User: " + user)
                //// Create Firepad.
            var firepad = Firepad.fromCodeMirror(firepadRef, codeMirror, {
                defaultText: '// JavaScript Editing with Firepad!\nfunction go() {\n  var message = "Hello, world.";\n  console.log(message);\n}'
            });
            //$('.greeting-id').append(data.id);
            //$('.greeting-content').append(data.content);
        });
    });

}
// Helper to get hash from end of URL or generate a random one.
function getExampleRef() {
    var ref = firebase.database().ref();
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
