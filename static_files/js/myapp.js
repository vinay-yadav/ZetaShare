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
    if ($('#id_password1').val() != $('#id_password2').val()) {
        $('#id_password2').css('border-color', 'red')
        $('#password2err').css('display', 'block')
        return false

    }

    return true
}


