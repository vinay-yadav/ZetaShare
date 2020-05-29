// Get CSRF Token
$(document).ready(function(){
    fetchAppList()
})
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
    }, { scope: 'manage_pages,publish_pages, pages_show_list' })
}

var userdata = {
    userId: '',
    name: '',
    email: '',
    userImg: '',
    AccessToken: ''
}

function isuserlogged(response) {
    userdata.AccessToken = response.authResponse.accessToken
    FB.api('/me', { fields: 'name, email, gender, picture' }, function (response) {
        userdata.userId = response.id
        userdata.name = response.name
        userdata.email = response.email
        userdata.userImg = response.picture.data.url
        
        $.ajax({
            method: 'post',
            url: '/app/connect-app/',
            data: userdata,
            headers: { "X-CSRFToken": getCookie('csrftoken') },
            success: function (res) {
                fetchAppList()
            }
        })
    })
}

function fetchAppList(){
    $.ajax({
        type:'get',
        url:'/app/connected/fetch/',
        async:false,
        success:function(res){
            createAppList(res)          
        }
    })
}

function createAppList(res){
    const ul = document.getElementById('setup-app')
    ul.innerHTML=""

    for(i in res.data){
    const li = document.createElement('li')
    li.setAttribute('class','app-list-item')

    const divappcontain = document.createElement('div')
    divappcontain.setAttribute('class','app-mainconatiner d-flex my-3 p-3')

    const appIcon = document.createElement('div')
    appIcon.setAttribute('class','app-icon')

    const iconImg = document.createElement('img')
    var iconattr = {
        src:'',
        alt:'',
        width:'40px',
        height:'40px'
    }
    if(res.data[i].provider ==='Facebook'){

        iconattr.src = '/static/images/icons8-facebook-50.png/'
        iconattr.alt = 'facebook-icon'
        var disconnect = document.createElement('div')
        disconnect.innerHTML = 'Disconnect'
        disconnectattrs = {
            'class':'btn btn-danger px-4 ',
            'id':res.data[i].posting_id,
            'onclick': 'disconnectApp(this)'
        }
         keyloop(disconnect,disconnectattrs)
    }
    if(res.data[i].provider ==='LinkedIn'){
        
        iconattr.src = '/static/images/linkedin.png'
        iconattr.alt = 'linkedin-icon'        
        var reconnect = document.createElement('div')
          reconnect.setAttribute('class','btn btn-primary px-4 ')
          reconnect.innerHTML = 'Reconnect'


        var disconnect = document.createElement('div')
        disconnectattrs = {
            'class':'btn btn-danger px-4 ml-3',
            'id':res.data[i].posting_id,
            'onclick': 'disconnectApp(this)'
        }
         keyloop(disconnect,disconnectattrs)
          disconnect.innerHTML = 'Disconnect'
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
        'value':res.data[i].page_name
    }

    keyloop(accName,nameattr)
      const divider = document.createElement('div')
      divider.setAttribute('class','divider')

      const span = document.createElement('span')
      span.setAttribute('class','app-createdAt')
      const date = new Date(res.data[i].added_on)
      date.toDateString()
      span.innerHTML = date

      const appbutton = document.createElement('div')
      appbutton.setAttribute('class','app-button mx-5')

      li.appendChild(divappcontain)
      divappcontain.appendChild(appIcon)
      divappcontain.appendChild(appInfo)
      divappcontain.appendChild(appbutton)
      if(res.data[i].provider === 'Facebook'){
        appbutton.appendChild(disconnect)
      }
      if(res.data[i].provider === 'LinkedIn'){
        appbutton.appendChild(reconnect)
        appbutton.appendChild(disconnect)
      }
      
      appIcon.appendChild(iconImg)
      appInfo.appendChild(buttonAcc)
      appInfo.appendChild(divider)
      appInfo.appendChild(span)
      buttonAcc.appendChild(icon)
      buttonAcc.appendChild(accNameDiv)
      accNameDiv.appendChild(accName)
      ul.appendChild(li)
    }
        

      
}

function keyloop(element,attrs){
    for(let i in attrs){
        element.setAttribute(i,attrs[i])

    }
}

// function for disconnect app

function disconnectApp(ref){
    $.ajax({
        type:'get',
        url:'/app/connected/delete/',
        data:{pid:ref.getAttribute('id')},
        success:function(res){
            createAppList(res)
        }
    })
}
