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

window.fbAsyncInit = function () {
    FB.init({
        // appId: '243240056787926',
        appId: '735133187228573',
        cookie: true,
        xfbml: true,
        version: 'v6.0'
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


function checkLoginState() {
    FB.getLoginStatus(function (response) {
        statusChangeCallback(response);
    });
}

function statusChangeCallback(response) {
    if (response.status === 'connected') {
        fetchdata();
    }
}



function fetchdata() {
    console.log('Welcome!  Fetching your information.... ');
    FB.api('/me', { fields: 'name, email, id, picture' }, function (response) {
        console.log(response)
        let user_data = {
            userId: response.id,
            userName: response.name,
            userEmail: response.email,
            userImg: response.picture.data.url,
            provider: 'Facebook'
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

// Google Login
function onSignIn(googleUser) {
    var profile = googleUser.getBasicProfile();
    // ajax to submit data to database
    const user_data = {
        userId: profile.getId(),
        userName: profile.getName(),
        userEmail: profile.getEmail(),
        userImg: profile.getImageUrl(),
        provider: 'Google'
        // accessToken: googleUser.getAuthResponse().access_token
    }

    $.ajax({
        type: 'post',
        url: '/social-auth/',
        data: user_data,
        headers: { "X-CSRFToken": getCookie('csrftoken') },
        success: function (res) {
            console.log('google')
            gLogout()
            window.location.replace(res.url)

        }
    })
}

function onFailure() {
    alert('not able to SignIn')
    window.location.replace(res.url)
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






