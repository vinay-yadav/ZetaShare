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

// create app
window.fbAsyncInit = function () {
    FB.init({
        // appId: '243240056787926',
        appId: '735133187228573',
        cookie: true,
        xfbml: true,
        version: 'v6.0'
    });

    FB.getLoginStatus(function (response) {
        statusCheck(response)
    })

};

(function (d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) { return; }
    js = d.createElement(s); js.id = id;
    js.src = "https://connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));




function CreateFacebookApp() {
    FB.login(function (response) {
        if (response.status === "connected") {
            isuserlogged(response)
        }
        statusCheck(response)
    }, { scope: 'manage_pages,publish_pages, pages_show_list' })
}

var userdata = {
    userId: '',
    name: '',
    email: '',
    AccessToken: ''
}
function statusCheck(response) {
    if (response.status === 'connected') {
        document.getElementById('fbconnect').setAttribute('onclick', 'LogoutFacebookApp()')
        document.getElementById('fbconnect').innerHTML = 'disconnect'


    }
    else {
        document.getElementById('fbconnect').setAttribute('onclick', 'CreateFacebookApp()')
        document.getElementById('fbconnect').innerHTML = 'Connect Your App'
    }
}

function isuserlogged(response) {
    userdata.AccessToken = response.authResponse.accessToken
    FB.api('/me', { fields: 'name, email, gender' }, function (response) {
        userdata.name = response.name
        userdata.userId = response.id
        userdata.email = response.email
        console.log(userdata)

        $.ajax({
            method: 'post',
            url: '/app/connect-app/',
            data: userdata,
            headers: { "X-CSRFToken": getCookie('csrftoken') },
            success: function (res) {
                console.log(res.msg)
            }
        })
    })
}
function LogoutFacebookApp() {
    document.getElementById('fbconnect').setAttribute('onclick', 'CreateFacebookApp()')
    document.getElementById('fbconnect').innerHTML = 'Connect Your App'
}


