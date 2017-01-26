/* global firebase, Firepad, $, CodeMirror */

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
            console.log("Data from API: " + JSON.stringify(token_data));
            // var cust_token = data['token']
            // console.log("Cust token: " + cust_token)
            firebase.initializeApp(config);
            //// Get Firebase Database reference.
            var firepadRef = getExampleRef();
            //// Create CodeMirror (with line numbers and the JavaScript mode).
            var user_details = {
                username: "",
                uid:""
            }
            var codeMirror = CodeMirror(document.getElementById('firepad-container'), {
                lineNumbers: true,
                lineWrapping: true,
                mode: 'python'
            });
            firebase.auth().signInWithCustomToken(token_data['token']).then(function(data) {
                // Authentication successful.
                console.log("Authentication successful!");
                console.log("Data: " + JSON.stringify(data));
                user_details.uid = data['uid']
                var userRef = firebase.database().ref('users/' + data['uid'] + '/username/');
                var firepad = Firepad.fromCodeMirror(firepadRef, codeMirror, {
                        defaultText: '# Welcome to Psquair: Start writing some Python Code',
                        userId: data['uid'],
                        richTextShortcuts: true
                    });
                userRef.on('value', function(snapshot) {
                    //   updateStarCount(postElement, snapshot.val());
                    console.log("Snapshot strinified: " +
                    String(snapshot.val()).charAt(0));
                    //   updateUIElement("aside #sidebar .sidebar-menu #current-user .name-initial"
                    //   ).text(snapshot.val())
                    var username = String(snapshot.val())
                    var init_char = username.charAt(0)
                    $("#sidebar .sidebar-menu #current-user .name-initial").text(init_char);
                    $("#sidebar .sidebar-menu #current-user .u-name").text(username);

                });
                // data['uid']
                var userList = FirepadUserList.fromDiv(firepadRef.child('users'),
                document.getElementById('firepad-userlist'), data['uid']);

            }, function(error) {
                var errorCode = error.code;
                var errorMessage = error.message;
                console.log(error)
            });
            // var user = firebase.auth().currentUser;
            // console.log("User: " + user)
            codeMirror.focus();
        });
    });

}
// Helper to get hash from end of URL or generate a random one.
function getExampleRef() {
    var ref = firebase.database().ref().child('pair_session');
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

function updateUIElement(elem, data) {
    console.log("Updating UI...");
    $(elem).text(data);

}