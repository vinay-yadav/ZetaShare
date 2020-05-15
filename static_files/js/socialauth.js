// Get CSRF Token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


// facebook login
function statusChangeCallback(response) {

    if (response.status === 'connected') {
        fetchdata();
        $('.glog').attr('onclick', 'fbLogout()')
        $('.login-sidebar').hide()

    }
    else {
        $('#user-info').css('display', 'none')
        $('.auth-button').css('display', 'block')                         // Not logged into your webpage or we are unable to tell.
    }
}


function checkLoginState() {               // Called when a person is finished with the Login Button.
    FB.getLoginStatus(function (response) {   // See the onlogin handler
        statusChangeCallback(response);
    });
}


window.fbAsyncInit = function () {
    FB.init({
        //appId: '243240056787926',
        appId: '735133187228573',
        cookie: true,                     // Enable cookies to allow the server to access the session.
        xfbml: true,                     // Parse social plugins on this webpage.
        version: 'v6.0'           // Use this Graph API version for this call.
    });


    FB.getLoginStatus(function (response) {   // Called after the JS SDK has been initialized.
        statusChangeCallback(response);        // Returns the login status.
    });
};


// Load the SDK asynchronously
(function (d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src = "https://connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));


function fetchdata() {                      // Testing Graph API after login.  See statusChangeCallback() for when this call is made.
    console.log('Welcome!  Fetching your information.... ');
    FB.api('/me', {fields: 'name, email, id'}, function (response) {
        console.log(response)
        document.getElementById('logged_user_name').innerHTML = response.name

        const user_data = {
            userId: response.id,
            userName: response.name,
            userEmail: response.email
        }
        console.log(user_data)
        $.ajax({
            type: 'post',
            url: "/social-auth/",
            data: user_data,
            headers: { "X-CSRFToken": getCookie('csrftoken') },
            success: function (res) {
                window.location.replace(res.url)
            }
        })

    });
}

function fbLogout() {
    FB.logout(function (response) {
        console.log('logout successfully')
        $('#user-info').css('display', 'none')
        $('.auth-button').css('display', 'block')
        location.reload()
    })
}


// Google Login
function onSignIn(googleUser) {
    var profile = googleUser.getBasicProfile();
    document.getElementById('logged_user_name').innerHTML = profile.getName()
    document.getElementById('user_profile_img').setAttribute('src', profile.getImageUrl())
    // $('#user-info').css('display', 'block')
    // $('.auth-button').css('display', 'none')
    $('.glog').attr('onclick', 'gLogout()')
    $('.login-sidebar').hide()

    // ajax to submit data to database
    const user_data = {
        userId: profile.getId(),
        userName: profile.getName(),
        userEmail: profile.getEmail(),
        userImg: profile.getImageUrl(),
        // accessToken: googleUser.getAuthResponse().access_token
    }

    $.ajax({
        type: 'post',
        url: '/social-auth/',
        data: user_data,
        headers: { "X-CSRFToken": getCookie('csrftoken') },
        success: function (res) {
            window.location.replace(res.url)
        }
    })
}

function onFailure() {
    alert('not able to SignIn')
    location.reload()
}


function renderButton() {
    gapi.signin2.render('googleauth', {
        'scope': 'profile email',
        'width': '250',
        'height': '40',
        'longtitle': true,
        'onsuccess': onSignIn,
        'onfailure': onFailure

    });
}
function gLogout() {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function () {
        console.log('User signed out.');
        console.log('logout successfully')
        $('#user-info').css('display', 'none')
        $('.auth-button').css('display', 'block')
        location.reload()
    });
}






