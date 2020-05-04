// Login Ajax
$(document).ready(function(){
    let $myForm = $("#auth-data")
    $myForm.submit(function(e){
        e.preventDefault();
        let $formData = $(this).serialize()
        let $endpoint = $myForm.attr("data-url")

        $.ajax({
            method: "POST",
            url: $endpoint,
            data: $formData,
            success: handleSuccess,
            error: handleError
        })

        function handleSuccess(data){
            alert(data['msg']);
            window.location.reload();
        }

        function handleError(data){
            let response = data.responseJSON.error.__all__[0]
            if (response === 'User does not exist') {
                $('#id_username').focus().css('background-color', 'red')
            } else if (response === 'Incorrect Password') {
                $('#id_password').focus().css('background-color', 'red')
            }
            else {
                alert(response)
            }
        }
    })
})


// User Registration Ajax
$(document).ready(function(){
    let $signupForm = $("#signup-user")
    $signupForm.submit(function(f){
        f.preventDefault();
        let $formData = $(this).serialize()
        let $endpoint = $signupForm.attr("data-url")

        $.ajax({
            method: "POST",
            url: $endpoint,
            data: $formData,
            success: handleSuccess,
            error: handleError
        })

        function handleSuccess(data){
            alert(data['msg']);
            window.location.reload();
        }

        function handleError(data){
            let response = data.responseJSON.error
            let key = Object.keys(response)[0]

            if (key === 'username'){
                $('#signup-user #id_username').focus().css('background-color', 'red')
                alert(response[key][0])
            }

            if (key === 'email'){
                alert(response[key][0])
                $('#id_email').focus().css('background-color', 'red')
            }

            if (key === 'password2'){
                alert(response[key][0])
            }
        }
    })
})



// nav active class
$(function () {
    $('#app-nav li a').click(function () {
        $("#app-nav li.active").removeClass('active')
        $('#app-nav li a').filter(function () {
            if ($(this).attr('href') == location.pathname) {
                $(this).parent().addClass('active')
            }
        })

    })
})

function slidertoggle() {
    $('.login-sidebar').toggle('slow')
}

// switch forms

$('#login').click(function () {
    $('.signup-user').hide()
    $('.auth-data').show()

})
$('#signup').click(function () {
    $('.auth-data').hide()
    $('.signup-user').show()

})

function loginSubmit() {
    const regex = /[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?/g
    if (regex.test($('#loginemail').val()) == false) {
        $("#loginemail").focus().css('border-color', 'red')

        // $("#loginemail").after("<p style='margin: 0;font-size: 10px;color: red;position: absolute;top: 24px;'>enter valid email address</p>")

        return false
    }
    $("#loginemail").css('border-color', '#e2d646')


    if ($('#loginpass').val() == '') {
        $('#loginpass').css('border-color', 'red')
        // $('#loginpass').after("<p style='margin: 0;font-size: 10px;color: red;position: absolute;top: 24px;  >enter valid password</p>")
        return false
    }
    $('#loginpass').css('border-color', '#e2d646')
    return true

}

function Signupvalidation() {
    const regex = /[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?/g
    if (regex.test($('#id_email').val()) == false) {
        $('#id_email').css('border-color', 'red')
        return false
    }
    if ($('#id_password1').val() !== $('#id_password2').val()) {
        $('#id_password2').css('border-color', 'red')
        $('#password2err').css('display', 'block')
        return false

    }

    return true
}
