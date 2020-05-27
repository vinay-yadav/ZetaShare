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
        appId: '243240056787926',
        // appId: '735133187228573',
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
    userImg: '',
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
    FB.api('/me', { fields: 'name, email, gender, picture' }, function (response) {
        userdata.userId = response.id
        userdata.name = response.name
        userdata.email = response.email
        userdata.userImg = response.picture.data.url
        console.log(userdata)

        $.ajax({
            method: 'post',
            url: '/app/connect-app/',
            data: userdata,
            headers: { "X-CSRFToken": getCookie('csrftoken') },
            success: function (res) {
                console.log()
            }
        })
    })
}
function LogoutFacebookApp() {
    document.getElementById('fbconnect').setAttribute('onclick', 'CreateFacebookApp()')
    document.getElementById('fbconnect').innerHTML = 'Connect Your App'
}


function fetchAppList(){
    $.ajax({
        type:'get',
        url:'/app/connected/fetch/',
        async:false,
        success:function(res){
            console.log(res)
            
        }
    })
}

function createAppList(){
    const ul = document.getElementById('setup-app')
    const li = document.createElement('li')
    li.setAttribute('class','app-list-item')

    const divappcontain = document.createElement('div')
    divappcontain.setAttribute('class','app-mainconatiner d-flex my-3 p-3')

    const appIcon = document.createElement('div')
    appIcon.setAttribute('class','app-icon')

    const iconImg = document.createElement('img')
    let iconattr = {
        'src':'/static/images/icons8-facebook-50.png',
        'alt':'facebook-icon',
        'width':'40px',
        'height':'40px'
    }
    keyloop(iconImg,iconattr)
    const appInfo = document.createElement('div')
    let infoattr = {
        'class':'app-info px-4',
        'style':'flex:1'
    }
    

    keyloop(appInfo,infoattr)
    const buttonAcc = document.createElement('div')
    let buttonattr = {
        'class':'button-acc w-100 d-flex',
        'style':'align-item:conter'
    }
    keyloop(buttonAcc,buttonattr)
    
    const icon = document.createElement('i')
    icon.setAttribute('class','bx bx-pencil')
    const accNameDiv = document.createElement('div')
    accNameDiv.setAttribute('class','acc-name pl-1')
    const accName = document.createElement('input')
    let nameattr = {
        'class':'account-name',
        'type':'text',
        'placeholder':'Account Name',
        'value':''
    }

    keyloop(accName,nameattr)
      const divider = document.createElement('div')
      divider.setAttribute('class','divider')

      const span = document.createElement('span')
      span.setAttribute('class','app-createdAt')
      span.innerHTML = 'Added On : 22/06/1999'
    
      li.appendChild(divappcontain)
      divappcontain.appendChild(appIcon)
      divappcontain.appendChild(appInfo)
      appIcon.appendChild(iconImg)
      appInfo.appendChild(buttonAcc)
      buttonAcc.appendChild(icon)
      buttonAcc.appendChild(accNameDiv)
      accNameDiv.appendChild(accName)
           
      ul.append(li)
}

function keyloop(element,attrs){
    for(let i in attrs){
        element.setAttribute(i,attrs[i])

    }
}

